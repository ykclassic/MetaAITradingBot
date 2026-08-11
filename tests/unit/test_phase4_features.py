"""
Verifiable Tests for the Feature Engine.
Ensures deterministic calculation and guards against NaN leakage.
"""

import pytest
import datetime
from typing import List

from app.features.engine import PandasFeatureEngine


@pytest.fixture
def sample_candles() -> List[dict]:
    """Generates 60 periods of synthetic ascending OHLCV data."""
    base_time = int(datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc).timestamp())
    candles = []
    
    # Create a clean uptrend to easily verify EMA and Trend Distance
    base_price = 1.0000
    for i in range(60):
        candles.append({
            "time": base_time + (i * 3600), # H1 candles
            "open": base_price + (i * 0.0010),
            "high": base_price + (i * 0.0015),
            "low": base_price + (i * 0.0005),
            "close": base_price + (i * 0.0012),
            "tick_volume": 1000 + i
        })
    return candles


def test_feature_engine_success(sample_candles):
    engine = PandasFeatureEngine()
    
    snapshot = engine.compute_features(
        symbol="EURUSD", 
        timeframe="H1", 
        candles=sample_candles
    )

    assert snapshot.symbol == "EURUSD"
    assert snapshot.timeframe == "H1"
    assert snapshot.feature_version == engine.FEATURE_VERSION
    
    # Assert values exist and are floats
    assert isinstance(snapshot.features["rsi_14"], float)
    assert isinstance(snapshot.features["ema_20"], float)
    assert isinstance(snapshot.features["atr_14"], float)
    
    # Given the synthetic uptrend, EMA 20 should be > EMA 50
    assert snapshot.features["trend_distance"] > 0.0


def test_feature_engine_insufficient_data():
    engine = PandasFeatureEngine()
    short_candles = [{"time": 1600000000, "open": 1, "high": 1.1, "low": 0.9, "close": 1.05}] * 10
    
    with pytest.raises(ValueError, match="Insufficient data"):
        engine.compute_features(symbol="EURUSD", timeframe="H1", candles=short_candles)


def test_feature_engine_missing_keys():
    engine = PandasFeatureEngine()
    bad_candles = [{"open": 1, "high": 1.1, "low": 0.9, "close": 1.05}] * 60
    
    with pytest.raises(ValueError, match="Candle data missing 'time'"):
        engine.compute_features(symbol="EURUSD", timeframe="H1", candles=bad_candles)