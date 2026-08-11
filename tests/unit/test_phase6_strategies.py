"""
Verifiable Tests for Strategy Logic and Regime Filtering.
"""

import pytest
from datetime import datetime, timezone

from app.domain.models import FeatureSnapshot, RegimeResult
from app.domain.enums import MarketRegime, SignalDirection
from app.strategies.implementations import EMATrendStrategy, RSIMeanReversionStrategy


@pytest.fixture
def base_regime():
    return RegimeResult(
        regime=MarketRegime.STRONG_TREND_UP,
        confidence=0.85,
        timestamp=datetime.now(timezone.utc),
        model_version="v1",
        feature_version="v1"
    )

@pytest.fixture
def trend_features():
    return FeatureSnapshot(
        timestamp=datetime.now(timezone.utc),
        symbol="EURUSD",
        timeframe="M15",
        features={
            "close": 1.1000,
            "ema_20": 1.1001,  # Close is very near EMA 20 (pullback)
            "ema_50": 1.0950,  # Trend is clearly up
            "rsi_14": 55.0,    # Not overbought
            "atr_14": 0.0020
        },
        feature_version="v1"
    )

def test_ema_trend_generates_buy_signal(trend_features, base_regime):
    strategy = EMATrendStrategy()
    signal = strategy.generate_signal(trend_features, base_regime)
    
    assert signal is not None
    assert signal.direction == SignalDirection.BUY
    assert signal.strategy_name == "EMA_Trend"
    # Check Math: SL = close - 1.5*ATR = 1.1000 - 0.0030 = 1.0970
    assert pytest.approx(signal.stop_loss) == 1.0970
    # Check Math: TP = close + 3.0*ATR = 1.1000 + 0.0060 = 1.1060
    assert pytest.approx(signal.take_profit) == 1.1060


def test_ema_trend_rejects_wrong_regime(trend_features):
    strategy = EMATrendStrategy()
    wrong_regime = RegimeResult(
        regime=MarketRegime.RANGE_LOW_VOL, 
        confidence=0.9, 
        timestamp=datetime.now(timezone.utc),
        model_version="v1", 
        feature_version="v1"
    )
    
    # Even though features are perfect for a trend pullback, the regime says RANGE
    signal = strategy.generate_signal(trend_features, wrong_regime)
    assert signal is None


def test_rsi_mean_reversion_oversold():
    strategy = RSIMeanReversionStrategy()
    
    regime = RegimeResult(
        regime=MarketRegime.RANGE_LOW_VOL, 
        confidence=0.8, timestamp=datetime.now(timezone.utc), 
        model_version="v1", feature_version="v1"
    )
    
    features = FeatureSnapshot(
        timestamp=datetime.now(timezone.utc), symbol="GBPUSD", timeframe="M15",
        features={"close": 1.2500, "rsi_14": 25.0, "atr_14": 0.0020}, # RSI < 30
        feature_version="v1"
    )
    
    signal = strategy.generate_signal(features, regime)
    assert signal is not None
    assert signal.direction == SignalDirection.BUY
    assert signal.strategy_name == "RSI_MeanReversion"


def test_strategy_raises_on_missing_features(base_regime):
    strategy = EMATrendStrategy()
    bad_features = FeatureSnapshot(
        timestamp=datetime.now(timezone.utc), symbol="EURUSD", timeframe="M15",
        features={"close": 1.1000}, # Missing EMAs, RSI, ATR
        feature_version="v1"
    )
    
    with pytest.raises(ValueError, match="missing required feature"):
        strategy.generate_signal(bad_features, base_regime)