"""Deterministic, broker-safe verification of the complete trading path."""

from datetime import datetime, timezone
from uuid import uuid4

from app.domain.enums import MarketRegime, SignalDirection
from app.domain.models import AccountState, FeatureSnapshot, RegimeResult, Signal
from app.execution.engine import ExecutionEngine
from app.pipeline.orchestrator import TradingPipeline
from app.risk.manager import StandardRiskManager


class FakeAdapter:
    def __init__(self):
        self.order_calls = 0

    def is_connected(self):
        return True

    def connect(self):
        return True

    def disconnect(self):
        pass

    def get_account_state(self):
        return AccountState(
            balance=10_000.0,
            equity=10_000.0,
            margin=0.0,
            free_margin=10_000.0,
            daily_start_equity=10_000.0,
            current_daily_drawdown_pct=0.0,
            open_positions_count=0,
        )

    def get_ohlcv(self, symbol, timeframe, count):
        return [{"close": 100.0, "open": 99.0, "high": 101.0, "low": 98.0, "time": 1.0, "tick_volume": 100.0}]

    def get_open_positions(self):
        return []

    def send_order(self, request):
        self.order_calls += 1
        raise AssertionError("Safe verification must never call the broker order endpoint")


class FakeFeatureEngine:
    def compute_features(self, symbol, timeframe, candles):
        return FeatureSnapshot(
            timestamp=datetime.now(timezone.utc),
            symbol=symbol,
            timeframe=timeframe,
            features={"close": 100.0, "atr_14": 1.0},
            feature_version="verification",
        )


class FakeRegimeDetector:
    def predict(self, features):
        return RegimeResult(
            regime=MarketRegime.RANGE_LOW_VOL,
            confidence=1.0,
            timestamp=datetime.now(timezone.utc),
            model_version="verification",
            feature_version=features.feature_version,
        )


class DeterministicSignalStrategy:
    def generate_signal(self, features, regime):
        return Signal(
            signal_id=uuid4(),
            timestamp=datetime.now(timezone.utc),
            symbol=features.symbol,
            timeframe=features.timeframe,
            direction=SignalDirection.BUY,
            entry_price=100.0,
            stop_loss=99.0,
            take_profit=102.0,
            strategy_name="DeterministicSafeVerification",
            strategy_version="1.0.0",
            signal_confidence=1.0,
        )


class SingleSignalSelector:
    def select_best_signal(self, signals):
        return signals[0] if signals else None


def test_safe_pipeline_reaches_signal_risk_and_execution_gate_without_order_submission(caplog):
    caplog.set_level("INFO")
    adapter = FakeAdapter()
    pipeline = TradingPipeline(
        adapter=adapter,
        feature_engine=FakeFeatureEngine(),
        regime_detector=FakeRegimeDetector(),
        strategies=[DeterministicSignalStrategy()],
        signal_selector=SingleSignalSelector(),
        risk_manager=StandardRiskManager(
            risk_per_trade_pct=0.01,
            max_daily_drawdown_pct=0.05,
            max_open_positions=3,
            contract_size=1.0,
        ),
        execution_engine=ExecutionEngine(adapter=adapter, live_trading_enabled=False),
        symbols=["BTC_USDT"],
        timeframe="M15",
        lookback_periods=1,
    )

    pipeline.run_cycle()

    messages = [record.getMessage() for record in caplog.records]
    assert any("MARKET DATA READY: BTC_USDT" in message for message in messages)
    assert any("FEATURES READY: BTC_USDT" in message for message in messages)
    assert any("SIGNAL SELECTED: BTC_USDT" in message for message in messages)
    assert any("RISK APPROVED: BTC_USDT" in message for message in messages)
    assert any("EXECUTION GATE REACHED: LIVE_TRADING_ENABLED=false" in message for message in messages)
    assert adapter.order_calls == 0
