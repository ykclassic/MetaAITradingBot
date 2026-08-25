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
        loaded = manager.load_model(version_id)
        self.model, self.mapping, self.preprocessing = loaded

        mean = self.preprocessing.get("feature_mean")
        std = self.preprocessing.get("feature_std")
        if mean is not None and std is not None:
            self.feature_mean = np.asarray(mean, dtype=float)
            self.feature_std = np.asarray(std, dtype=float)
            if self.feature_mean.shape != (4,) or self.feature_std.shape != (4,):
                raise ValueError("Invalid persisted HMM preprocessing metadata")
            self.feature_std = np.where(self.feature_std < 1e-12, 1.0, self.feature_std)
        else:
            self.feature_mean = None
            self.feature_std = None

    def predict(self, snapshot: FeatureSnapshot) -> RegimeResult:
        try:
            raw = np.array([[
                snapshot.features["trend_distance"],
                snapshot.features["atr_14"],
                snapshot.features["rsi_14"],
                snapshot.features["bb_width_20"],
            ]], dtype=float)
        except KeyError as e:
            raise ValueError(f"FeatureSnapshot missing required feature for HMM: {e}")

        if not np.isfinite(raw).all():
            raise ValueError("FeatureSnapshot contains non-finite HMM inputs")

        X = raw
        if self.feature_mean is not None and self.feature_std is not None:
            X = (raw - self.feature_mean) / self.feature_std

        probabilities = self.model.predict_proba(X)[0]
        best_state = int(np.argmax(probabilities))
        confidence = float(probabilities[best_state])

        if confidence < self.confidence_threshold:
            detected_regime = MarketRegime.UNKNOWN
        else:
            detected_regime = self.mapping.get(best_state, MarketRegime.UNKNOWN)

        return RegimeResult(
            regime=detected_regime,
            confidence=confidence,
            timestamp=datetime.now(timezone.utc),
            model_version=self.version_id,
            feature_version=snapshot.feature_version,
        )
