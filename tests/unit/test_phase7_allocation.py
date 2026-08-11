"""
Verifiable Tests for the Strategy Selector.
Ensures conflict resolution and confidence ranking work deterministically.
"""

import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone, timedelta

from app.allocation.selector import ConfidenceBasedSelector
from app.domain.models import FeatureSnapshot, RegimeResult, Signal
from app.domain.enums import MarketRegime, SignalDirection


@pytest.fixture
def dummy_context():
    features = FeatureSnapshot(
        timestamp=datetime.now(timezone.utc),
        symbol="EURUSD", timeframe="H1",
        features={"close": 1.1000}, feature_version="v1"
    )
    regime = RegimeResult(
        regime=MarketRegime.STRONG_TREND_UP, confidence=0.8,
        timestamp=datetime.now(timezone.utc), model_version="v1", feature_version="v1"
    )
    return features, regime


def create_mock_strategy(name: str, direction: SignalDirection, confidence: float, returns_signal: bool = True):
    strategy = MagicMock()
    strategy.name = name
    
    if returns_signal:
        signal = Signal(
            symbol="EURUSD", timeframe="H1", direction=direction,
            entry_price=1.1000, stop_loss=1.0950, take_profit=1.1100,
            strategy_name=name, strategy_version="v1", signal_confidence=confidence,
            expiration=datetime.now(timezone.utc) + timedelta(minutes=15)
        )
        strategy.generate_signal.return_value = signal
    else:
        strategy.generate_signal.return_value = None
        
    return strategy


def test_selector_highest_confidence_wins(dummy_context):
    features, regime = dummy_context
    
    strat1 = create_mock_strategy("Strat_A", SignalDirection.BUY, 0.75)
    strat2 = create_mock_strategy("Strat_B", SignalDirection.BUY, 0.90)  # Highest confidence
    strat3 = create_mock_strategy("Strat_C", SignalDirection.BUY, 0.85)
    
    selector = ConfidenceBasedSelector(strategies=[strat1, strat2, strat3])
    winning_signal = selector.evaluate(features, regime)
    
    assert winning_signal is not None
    assert winning_signal.strategy_name == "Strat_B"
    assert winning_signal.signal_confidence == 0.90


def test_selector_resolves_conflict_by_discarding(dummy_context):
    features, regime = dummy_context
    
    strat1 = create_mock_strategy("Strat_A", SignalDirection.BUY, 0.95)
    strat2 = create_mock_strategy("Strat_B", SignalDirection.SELL, 0.80)  # Conflicting direction
    
    selector = ConfidenceBasedSelector(strategies=[strat1, strat2])
    winning_signal = selector.evaluate(features, regime)
    
    # Conflicting directions must result in None to protect capital
    assert winning_signal is None


def test_selector_handles_no_signals(dummy_context):
    features, regime = dummy_context
    
    strat1 = create_mock_strategy("Strat_A", SignalDirection.BUY, 0.0, returns_signal=False)
    strat2 = create_mock_strategy("Strat_B", SignalDirection.SELL, 0.0, returns_signal=False)
    
    selector = ConfidenceBasedSelector(strategies=[strat1, strat2])
    winning_signal = selector.evaluate(features, regime)
    
    assert winning_signal is None


def test_selector_survives_strategy_crash(dummy_context):
    features, regime = dummy_context
    
    strat1 = create_mock_strategy("Strat_A", SignalDirection.BUY, 0.85)
    
    # Mock a strategy that throws an exception
    strat_crash = MagicMock()
    strat_crash.name = "Strat_Crash"
    strat_crash.generate_signal.side_effect = ValueError("Division by zero in indicator")
    
    selector = ConfidenceBasedSelector(strategies=[strat1, strat_crash])
    winning_signal = selector.evaluate(features, regime)
    
    # The selector should catch the error and still process strat1
    assert winning_signal is not None
    assert winning_signal.strategy_name == "Strat_A"