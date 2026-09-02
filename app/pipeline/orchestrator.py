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
        monitor=None,
        performance_tracker=None,
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
        self.monitor = monitor
        self.performance_tracker = performance_tracker
        self.is_running = False
        self._startup_notified = False
        self._shutdown_notified = False

    def _journal(self, method: str, *args, **kwargs) -> None:
        """Persistence/analytics failures must not interrupt the trading pipeline."""
        if not self.performance_tracker:
            return
        try:
            getattr(self.performance_tracker, method)(*args, **kwargs)
        except Exception as exc:
            logger.warning("Performance journal write failed: %s", exc)

    def _notify_startup(self) -> None:
        if self.monitor and not self._startup_notified:
            self.monitor.startup(self.symbols, self.timeframe, self.execution_engine.live_trading_enabled)
            self._startup_notified = True

    def run_cycle(self) -> None:
        """Execute one complete pass; infrastructure/authentication failures are fatal."""
        if not self.adapter.is_connected():
            raise ConnectionError("Adapter is disconnected. Cannot execute trading cycle.")

        self._notify_startup()
        cycle_started = time.monotonic()
        signal_count = approved_count = execution_count = 0
        logger.info("TRADING CYCLE START: symbols=%s timeframe=%s", ",".join(self.symbols), self.timeframe)
        if self.monitor:
            self.monitor.cycle_started(self.symbols, self.timeframe)

        account_state = self.adapter.get_account_state()
        logger.info(
            "ACCOUNT STATE READY: equity=%s available=%s open_orders=%s drawdown=%s",
            account_state.equity,
            account_state.free_margin,
            account_state.open_positions_count,
            account_state.current_daily_drawdown_pct,
        )
        if self.monitor:
            self.monitor.account_state(account_state)

        for symbol in self.symbols:
            result = self._process_symbol(symbol, account_state)
            signal_count += result[0]
            approved_count += result[1]
            execution_count += result[2]

        duration = time.monotonic() - cycle_started
        self._journal("record_cycle", duration, self.symbols, signal_count, approved_count, execution_count)
        logger.info("TRADING CYCLE COMPLETE: duration=%.3fs signals=%d approved=%d executions=%d", duration, signal_count, approved_count, execution_count)
        if self.monitor:
            self.monitor.cycle_completed(len(self.symbols), signal_count, approved_count, execution_count, duration)

    def _process_symbol(self, symbol: str, account_state: "AccountState") -> tuple[int, int, int]:
        signal_count = approved_count = execution_count = 0
        logger.info("SYMBOL START: %s", symbol)
        try:
            candles = self.adapter.get_ohlcv(symbol, self.timeframe, self.lookback_periods)
            if not candles:
                logger.warning("MARKET DATA EMPTY: %s", symbol)
                if self.monitor:
                    self.monitor.symbol_update(symbol, "MARKET DATA EMPTY")
                return 0, 0, 0
            logger.info("MARKET DATA READY: %s candles=%d", symbol, len(candles))
            if self.monitor:
                self.monitor.symbol_update(symbol, "MARKET DATA READY", candles=len(candles))

            features = self.feature_engine.compute_features(symbol, self.timeframe, candles)
            logger.info("FEATURES READY: %s", symbol)

            regime = self.regime_detector.predict(features)
            logger.info("REGIME READY: %s", symbol)

            signals = []
            for strategy in self.strategies:
                signal = strategy.generate_signal(features, regime)
                if signal:
                    signals.append(signal)
                    self._journal("record_signal", signal, regime=regime.regime.value)
            signal_count = len(signals)
            logger.info("SIGNAL EVALUATION: %s candidates=%d", symbol, signal_count)
            if not signals:
                logger.info("NO TRADE SIGNAL: %s", symbol)
                if self.monitor:
                    self.monitor.symbol_update(symbol, "NO TRADE SIGNAL", candidates=0)
                return signal_count, 0, 0

            best_signal = self.signal_selector.select_best_signal(signals)
            if not best_signal:
                logger.info("SIGNAL ARBITRATION REJECTED: %s", symbol)
                if self.monitor:
                    self.monitor.symbol_update(symbol, "SIGNAL ARBITRATION REJECTED", candidates=signal_count)
                return signal_count, 0, 0
            logger.info("SIGNAL SELECTED: %s direction=%s", symbol, best_signal.direction.value)

            order_request = self.risk_manager.evaluate_signal(best_signal, account_state)
            if not order_request:
                logger.info("RISK REJECTED: %s", symbol)
                if self.monitor:
                    self.monitor.symbol_update(symbol, "RISK REJECTED")
                return signal_count, 0, 0
            approved_count = 1
            logger.info(
                "RISK APPROVED: %s quantity=%s entry=%s stop=%s target=%s",
                symbol,
                order_request.volume,
                order_request.price,
                order_request.stop_loss,
                order_request.take_profit,
            )

            execution_count = 1
            result = self.execution_engine.execute_order(order_request)
            self._journal("record_execution", result, symbol=symbol)
            logger.info("EXECUTION RESULT: %s state=%s order_id=%s", symbol, result.execution_state.value, result.order_id)
            if self.monitor:
                self.monitor.symbol_update(
                    symbol,
                    "EXECUTION RESULT",
                    state=result.execution_state.value,
                    order_id=result.order_id,
                    fill_price=result.fill_price,
                    filled_volume=result.filled_volume,
                )
            if result.execution_state == OrderExecutionState.EXECUTION_UNCERTAIN:
                logger.critical("Execution uncertain for %s. Manual review required.", symbol)
                if self.monitor:
                    self.monitor.error("EXECUTION UNCERTAIN", f"XT order state could not be confirmed for {symbol}.", critical=True)
                self.is_running = False
            return signal_count, approved_count, execution_count
        except Exception as exc:
            logger.error("Error processing symbol %s", symbol, exc_info=True)
            if self.monitor:
                self.monitor.error("SYMBOL PROCESSING ERROR", f"{symbol}: {exc}", critical=True)
            return signal_count, approved_count, execution_count

    def start(self, cycle_interval_seconds: int = 60) -> None:
        """Start the continuous trading loop."""
        self.is_running = True
        logger.info("Starting the Trading Pipeline...")
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
        if self.monitor and not self._shutdown_notified:
            self.monitor.shutdown()
            self._shutdown_notified = True
        logger.info("Trading Pipeline stopped safely.")
