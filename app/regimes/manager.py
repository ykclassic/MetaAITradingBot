"""
Manages HMM model training, persistence, versioning, and state mapping.
"""

import json
import os
from typing import Dict, Iterable, Tuple

import joblib
import numpy as np
import pandas as pd
from hmmlearn import hmm

from app.domain.enums import MarketRegime
from app.features.engine import PandasFeatureEngine


class ModelManager:
    TRAIN_COLS = ["trend_distance", "atr_14", "rsi_14", "bb_width_20"]
    MAPPING_SCHEMA_VERSION = 2
    MIN_COVARIANCE = 1e-6

    def __init__(self, model_dir: str = "models/"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)

    def train_and_save(self, features_df: pd.DataFrame, version_id: str) -> None:
        """Train a numerically stable HMM and persist its preprocessing metadata."""
        frame = features_df.copy()
        X = frame[self.TRAIN_COLS].astype(float).to_numpy()
        if not np.isfinite(X).all():
            raise ValueError("HMM training features contain non-finite values")
        if len(X) < 50:
            raise ValueError(f"Insufficient feature history to train HMM: {len(X)} samples")

        mean = X.mean(axis=0)
        std = X.std(axis=0)
        std = np.where(std < 1e-12, 1.0, std)
        X_scaled = (X - mean) / std

        model = hmm.GaussianHMM(
            n_components=4,
            covariance_type="diag",
            n_iter=300,
            random_state=42,
            min_covar=self.MIN_COVARIANCE,
        )
        model.fit(X_scaled)

        # hmmlearn can still learn a zero/near-zero diagonal variance for a state
        # with insufficiently diverse observations. Clamp it to a small positive
        # value so the persisted model remains valid for Cholesky/log-density work.
        model.covars_ = np.maximum(np.asarray(model.covars_, dtype=float), self.MIN_COVARIANCE)
        if not np.isfinite(model.covars_).all():
            raise ValueError("HMM training produced non-finite covariance values")
        if (model.covars_ < self.MIN_COVARIANCE).any():
            raise ValueError("HMM covariance stabilization failed")

        states = model.predict(X_scaled)
        frame["state"] = states
        mapping = self._map_states_to_regimes(frame)

        model_path = os.path.join(self.model_dir, f"hmm_v_{version_id}.joblib")
        mapping_path = os.path.join(self.model_dir, f"mapping_v_{version_id}.json")

        joblib.dump(model, model_path)
        payload = {
            "schema_version": self.MAPPING_SCHEMA_VERSION,
            "states": {str(k): v.value for k, v in mapping.items()},
            "feature_columns": self.TRAIN_COLS,
            "feature_mean": mean.tolist(),
            "feature_std": std.tolist(),
        }
        with open(mapping_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)

    def bootstrap_from_candles(
        self,
        candles_by_symbol: Dict[str, Iterable[dict]],
        version_id: str,
        timeframe: str,
    ) -> None:
        """
        Build a verification-only model from fresh exchange candles.

        Production/live execution must still provision a reviewed model artifact
        rather than auto-training one.
        """
        engine = PandasFeatureEngine()
        rows = []

        for symbol, candles in candles_by_symbol.items():
            candle_list = list(candles)
            if len(candle_list) < engine.MIN_CANDLES:
                raise ValueError(
                    f"Cannot bootstrap model for {symbol}: need at least "
                    f"{engine.MIN_CANDLES} candles, got {len(candle_list)}"
                )

            for end in range(engine.MIN_CANDLES, len(candle_list) + 1):
                snapshot = engine.compute_features(symbol, timeframe, candle_list[:end])
                rows.append(snapshot.features)

        if len(rows) < 50:
            raise ValueError(
                f"Insufficient feature history to bootstrap HMM: {len(rows)} samples"
            )

        features_df = pd.DataFrame(rows).dropna()
        self.train_and_save(features_df, version_id)

    def _map_states_to_regimes(self, df: pd.DataFrame) -> Dict[int, MarketRegime]:
        """Analyze state statistics to map arbitrary HMM integers to domain regimes."""
        stats = df.groupby("state").agg(
            {"trend_distance": "mean", "atr_14": "mean"}
        )
        median_vol = stats["atr_14"].median()
        mapping = {}

        for state in stats.index:
            mean_trend = stats.loc[state, "trend_distance"]
            mean_vol = stats.loc[state, "atr_14"]
            if mean_trend > 0.001:
                mapping[state] = MarketRegime.STRONG_TREND_UP
            elif mean_trend < -0.001:
                mapping[state] = MarketRegime.STRONG_TREND_DOWN
            elif mean_vol > median_vol:
                mapping[state] = MarketRegime.RANGE_HIGH_VOL
            else:
                mapping[state] = MarketRegime.RANGE_LOW_VOL
        return mapping

    def load_model(
        self, version_id: str
    ) -> Tuple[hmm.GaussianHMM, Dict[int, MarketRegime], dict]:
        """Load a model, its regime mapping, and preprocessing metadata."""
        model_path = os.path.join(self.model_dir, f"hmm_v_{version_id}.joblib")
        mapping_path = os.path.join(self.model_dir, f"mapping_v_{version_id}.json")

        if not os.path.exists(model_path) or not os.path.exists(mapping_path):
            raise FileNotFoundError(f"Model version {version_id} missing files.")

        model = joblib.load(model_path)
        with open(mapping_path, "r", encoding="utf-8") as f:
            raw_map = json.load(f)

        if "states" in raw_map:
            mapping_raw = raw_map["states"]
            metadata = raw_map
        else:
            mapping_raw = raw_map
            metadata = {}

        mapping = {int(k): MarketRegime(v) for k, v in mapping_raw.items()}
        return model, mapping, metadata
