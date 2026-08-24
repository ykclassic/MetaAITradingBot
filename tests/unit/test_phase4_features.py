"""Feature engine regression tests."""

import datetime
from typing import List

import pytest

from app.features.engine import PandasFeatureEngine


@pytest.fixture
def sample_candles() -> List[dict]:
    base_time = int(datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc).timestamp())
    return [
        {
            "time": base_time + (i * 3600),
            "open": 1.0 + i * 0.0010,
            "high": 1.0 + i * 0.0015,
            "low": 1.0 + i * 0.0005,
            "close": 1.0 + i * 0.0012,
            "tick_volume": 1000 + i,
        }
        for i in range(60)
    ]


def test_feature_engine_success(sample_candles):
    engine = PandasFeatureEngine()
    snapshot = engine.compute_features("EURUSD", "H1", sample_candles)
    assert snapshot.symbol == "EURUSD"
    assert snapshot.timeframe == "H1"
    assert snapshot.feature_version == engine.FEATURE_VERSION
    assert isinstance(snapshot.features["rsi_14"], float)
    assert isinstance(snapshot.features["ema_20"], float)
    assert isinstance(snapshot.features["atr_14"], float)
    assert snapshot.features["trend_distance"] > 0.0


def test_feature_engine_insufficient_data():
    engine = PandasFeatureEngine()
    candles = [{"time": 1600000000, "open": 1, "high": 1.1, "low": 0.9, "close": 1.05, "tick_volume": 1}] * 10
    with pytest.raises(ValueError, match="Insufficient data"):
        engine.compute_features("EURUSD", "H1", candles)


def test_feature_engine_missing_keys():
    engine = PandasFeatureEngine()
    candles = [{"open": 1, "high": 1.1, "low": 0.9, "close": 1.05, "tick_volume": 1}] * 60
    with pytest.raises(ValueError, match="Candle data missing 'time'"):
        engine.compute_features("EURUSD", "H1", candles)
