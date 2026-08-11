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
    RiskManagerProtocol
)
from app.execution.engine import ExecutionEngine
from app.domain.enums import ConnectionState, OrderExecutionState

logger = logging.getLogger(__name__)


class TradingPipeline:
    """
    Orchestrates the end-to-end trading loop for a given universe of symbols.
    """

    def __init__(self,
                 adapter: MarketDataAdapter,
                 feature_engine: FeatureEngineProtocol,
                 regime_detector: RegimeDetectorProtocol,
                 strategies: List[StrategyProtocol],
                 signal_selector: SignalSelectorProtocol,
                 risk_manager: RiskManagerProtocol,
                 execution_engine: ExecutionEngine,
                 symbols: List[str],
                 timeframe: str = "M15",
                 lookback_periods: int = 100):
        
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
        """Executes a single pass of the pipeline for all configured symbols."""
        if not self.adapter.is_connected():
            logger.error("Adapter is disconnected. Halting pipeline cycle.")
            return

        try:
            account_state = self.adapter.get_account_state()
        except Exception as e:
            logger.error(f"Failed to fetch account state: {e}")
            return

        for symbol in self.symbols:
            self._process_symbol(symbol, account_state)

    def _process_symbol(self, symbol: str, account_state: 'AccountState') -> None:
        """Processes the pipeline sequence for a single symbol."""
        logger.debug(f"Starting pipeline evaluation for {symbol}")
        
        try:
            # 1. Fetch Market Data
            candles = self.adapter.get_ohlcv(symbol, self.timeframe, self.lookback_periods)
            if not candles:
                logger.warning(f"No market data returned for {symbol}. Skipping.")
                return

            # 2. Compute Features
            features = self.feature_engine.compute_features(symbol, self.timeframe, candles)

            # 3. Detect Regime
            regime = self.regime_detector.predict(features)

            # 4. Generate Signals from all strategies
            signals = []
            for strategy in self.strategies:
                signal = strategy.generate_signal(features, regime)
                if signal:
                    signals.append(signal)

            if not signals:
                return

            # 5. Arbitrate Signals
            best_signal = self.signal_selector.select_best_signal(signals)
            if not best_signal:
                return

            # 6. Evaluate Risk & Size Position
            order_request = self.risk_manager.evaluate_signal(best_signal, account_state)
            if not order_request:
                return

            # 7. Execute Trade
            result = self.execution_engine.execute_order(order_request)
            
            # 8. Handle Critical Execution Failures
            if result.execution_state == OrderExecutionState.EXECUTION_UNCERTAIN:
                logger.critical(f"Execution uncertain for {symbol}. Manual review required.")
                self.is_running = False # Trigger safe shutdown

        except Exception as e:
            logger.error(f"Error processing symbol {symbol}: {e}", exc_info=True)

    def start(self, cycle_interval_seconds: int = 60) -> None:
        """Starts the continuous trading loop."""
        self.is_running = True
        logger.info("Starting Trading Pipeline...")
        
        if not self.adapter.connect():
            logger.critical("Failed to connect to the broker. Aborting startup.")
            return

        try:
            while self.is_running:
                self.run_cycle()
                
                # Check if running flag was altered during the cycle (e.g., by a critical failure)
                if self.is_running:
                    time.sleep(cycle_interval_seconds)
                    
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Initiating graceful shutdown.")
        finally:
            self.stop()

    def stop(self) -> None:
        """Safely stops the pipeline and disconnects the adapter."""
        self.is_running = False
        self.adapter.disconnect()
        logger.info("Trading Pipeline stopped safely.")