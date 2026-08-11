"""
Implementation of the RegimeDetectorProtocol.
Executes inference on incoming feature snapshots.
"""

import numpy as np
from datetime import datetime, timezone

from app.core.interfaces import RegimeDetectorProtocol
from app.domain.models import FeatureSnapshot, RegimeResult
from app.domain.enums import MarketRegime
from app.regimes.manager import ModelManager


class HMMRegimeDetector(RegimeDetectorProtocol):
    def __init__(self, manager: ModelManager, version_id: str, confidence_threshold: float = 0.65):
        self.version_id = version_id
        self.confidence_threshold = confidence_threshold
        self.model, self.mapping = manager.load_model(version_id)

    def predict(self, snapshot: FeatureSnapshot) -> RegimeResult:
        # Extract features in the exact order the model was trained on
        try:
            X = np.array([[
                snapshot.features["trend_distance"],
                snapshot.features["atr_14"],
                snapshot.features["rsi_14"],
                snapshot.features["bb_width_20"]
            ]])
        except KeyError as e:
            raise ValueError(f"FeatureSnapshot missing required feature for HMM: {e}")

        # predict_proba returns array of shape (1, n_components)
        probabilities = self.model.predict_proba(X)[0]
        
        best_state = int(np.argmax(probabilities))
        confidence = float(probabilities[best_state])

        # Apply confidence threshold
        if confidence < self.confidence_threshold:
            detected_regime = MarketRegime.UNKNOWN
        else:
            detected_regime = self.mapping.get(best_state, MarketRegime.UNKNOWN)

        return RegimeResult(
            regime=detected_regime,
            confidence=confidence,
            timestamp=datetime.now(timezone.utc),
            model_version=self.version_id,
            feature_version=snapshot.feature_version
        )