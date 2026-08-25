"""
Main System Orchestrator.
Wires together all domain engines and executes the linear trading pipeline.
"""

import logging
import time
from typing import List

from app.core.interfaces import (
    MarketDataAdapter,
    FeatureEngineProtocol,
    RegimeDetectorProtocol,
    StrategyProtocol,
    SignalSelectorProtocol,
    RiskManagerProtocol,
)
from app.execution.engine import ExecutionEngine
from app.domain.enums import OrderExecutionState

logger = logging.getLogger(__name__)


class TradingPipeline:
    """Orchestrates the end-to-end trading loop for a configured symbol universe."""

    def __init__(
        self,
        adapter: MarketDataAdapter,
        feature_engine: FeatureEngineProtocol,
        regime_detector: RegimeDetectorProtocol,
        strategies: List[StrategyProtocol],
        signal_selector: SignalSelectorProtocol,
        risk_manager: RiskManagerProtocol,
        execution_engine: ExecutionEngine,
        symbols: List[str],
        timeframe: str = "M15",
        lookback_periods: int = 100,
    ):
        self.adapter = adapter
        self.feature_engine = feature_engine
        self.regime_detector = regime_detector
        self.strategies = strategies
        self.signal_selector = signal_selector
        self.risk_manager = risk_manager
        self.execution_engine = execution_engine
        self.symbols = symbols
        self.timeframe = timeframe
        self.lookback_periods = lookback_periods
        self.is_running = False

    def run_cycle(self) -> None:
        """Execute one complete pass; infrastructure/authentication failures are fatal."""
        if not self.adapter.is_connected():
            raise ConnectionError("Adapter is disconnected. Cannot execute trading cycle.")

        # Do not swallow account-state failures: a green process with no authenticated
        # account state would falsely report a successful trading-cycle verification.
        account_state = self.adapter.get_account_state()

        for symbol in self.symbols:
            self._process_symbol(symbol, account_state)

    def _process_symbol(self, symbol: str, account_state: "AccountState") -> None:
        logger.debug("Starting pipeline evaluation for %s", symbol)

        try:
            candles = self.adapter.get_ohlcv(symbol, self.timeframe, self.lookback_periods)
            if not candles:
                logger.warning("No market data returned for %s. Skipping.", symbol)
                return

            features = self.feature_engine.compute_features(symbol, self.timeframe, candles)
            regime = self.regime_detector.predict(features)

            signals = []
            for strategy in self.strategies:
                signal = strategy.generate_signal(features, regime)
                if signal:
                    signals.append(signal)

            if not signals:
                logger.info("No strategy signal for %s.", symbol)
                return

            best_signal = self.signal_selector.select_best_signal(signals)
            if not best_signal:
                logger.info("Signal arbitration rejected all signals for %s.", symbol)
                return

            order_request = self.risk_manager.evaluate_signal(best_signal, account_state)
            if not order_request:
                logger.info("Risk manager rejected signal for %s.", symbol)
                return

            result = self.execution_engine.execute_order(order_request)
            if result.execution_state == OrderExecutionState.EXECUTION_UNCERTAIN:
                logger.critical("Execution uncertain for %s. Manual review required.", symbol)
                self.is_running = False

        except Exception:
            logger.error("Error processing symbol %s", symbol, exc_info=True)
            # A per-symbol failure should not conceal that the overall cycle failed.
            raise

    def start(self, cycle_interval_seconds: int = 60) -> None:
        """Start the continuous trading loop."""
        self.is_running = True
        logger.info("Starting Trading Pipeline...")

        if not self.adapter.connect():
            raise ConnectionError("Failed to connect to the broker. Aborting startup.")

        try:
            while self.is_running:
                self.run_cycle()
                if self.is_running:
                    time.sleep(cycle_interval_seconds)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Initiating graceful shutdown.")
        finally:
            self.stop()

    def stop(self) -> None:
        """Safely stop the pipeline and disconnect the adapter."""
        self.is_running = False
        self.adapter.disconnect()
        logger.info("Trading Pipeline stopped safely.")
