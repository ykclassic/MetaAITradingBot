"""
Verifiable Tests for the Regime Engine.
Ensures mapping logic holds and confidence thresholds properly fallback to UNKNOWN.
"""

import pytest
import numpy as np
from unittest.mock import MagicMock
from datetime import datetime, timezone

from app.domain.models import FeatureSnapshot, RegimeResult
from app.domain.enums import MarketRegime
from app.regimes.hmm_detector import HMMRegimeDetector


@pytest.fixture
def dummy_snapshot():
    return FeatureSnapshot(
        timestamp=datetime.now(timezone.utc),
        symbol="EURUSD",
        timeframe="H1",
        features={
            "trend_distance": 0.002,
            "atr_14": 0.0015,
            "rsi_14": 65.0,
            "bb_width_20": 0.004,
            "ema_20": 1.100,
            "ema_50": 1.095,
            "close": 1.105,
            "volume": 1500
        },
        feature_version="1.0.0"
    )

@pytest.fixture
def mock_model_manager():
    manager = MagicMock()
    
    # Mock HMM model
    mock_hmm = MagicMock()
    # Simulate high confidence for state 0 (90%)
    mock_hmm.predict_proba.return_value = np.array([[0.90, 0.05, 0.03, 0.02]])
    
    # Mock Mapping: State 0 = STRONG_TREND_UP
    mock_mapping = {
        0: MarketRegime.STRONG_TREND_UP,
        1: MarketRegime.STRONG_TREND_DOWN,
        2: MarketRegime.RANGE_HIGH_VOL,
        3: MarketRegime.RANGE_LOW_VOL
    }
    
    manager.load_model.return_value = (mock_hmm, mock_mapping)
    return manager


def test_regime_detection_high_confidence(mock_model_manager, dummy_snapshot):
    detector = HMMRegimeDetector(
        manager=mock_model_manager, 
        version_id="test_v1", 
        confidence_threshold=0.65
    )
    
    result = detector.predict(dummy_snapshot)
    
    assert result.regime == MarketRegime.STRONG_TREND_UP
    assert result.confidence == 0.90
    assert result.model_version == "test_v1"
    assert result.feature_version == "1.0.0"


def test_regime_detection_low_confidence(mock_model_manager, dummy_snapshot):
    # Adjust mock to simulate uncertainty (max prob = 40%)
    mock_model_manager.load_model.return_value[0].predict_proba.return_value = np.array([[0.40, 0.30, 0.20, 0.10]])
    
    detector = HMMRegimeDetector(
        manager=mock_model_manager, 
        version_id="test_v1", 
        confidence_threshold=0.65
    )
    
    result = detector.predict(dummy_snapshot)
    
    # Even though state 0 is highest, confidence < threshold forces UNKNOWN
    assert result.regime == MarketRegime.UNKNOWN
    assert result.confidence == 0.40


def test_regime_detection_missing_features(mock_model_manager):
    detector = HMMRegimeDetector(mock_model_manager, "test_v1")
    
    bad_snapshot = FeatureSnapshot(
        timestamp=datetime.now(timezone.utc),
        symbol="EURUSD",
        timeframe="H1",
        features={"rsi_14": 50.0}, # Missing trend_distance, atr_14, bb_width_20
        feature_version="1.0.0"
    )
    
    with pytest.raises(ValueError, match="missing required feature"):
        detector.predict(bad_snapshot)