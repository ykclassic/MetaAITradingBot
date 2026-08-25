"""
Manages HMM model training, persistence, versioning, and state mapping.
"""

import json
import os
from typing import Dict, Iterable, Tuple

import joblib
import pandas as pd
from hmmlearn import hmm

from app.domain.enums import MarketRegime
from app.features.engine import PandasFeatureEngine


class ModelManager:
    def __init__(self, model_dir: str = "models/"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)

    def train_and_save(self, features_df: pd.DataFrame, version_id: str) -> None:
        """Trains the HMM and maps states to regimes based on statistical profiles."""
        n_components = 4
        model = hmm.GaussianHMM(
            n_components=n_components,
            covariance_type="full",
            n_iter=100,
            random_state=42,
        )

        train_cols = ["trend_distance", "atr_14", "rsi_14", "bb_width_20"]
        X = features_df[train_cols].astype(float).values
        model.fit(X)
        states = model.predict(X)
        features_df = features_df.copy()
        features_df["state"] = states

        mapping = self._map_states_to_regimes(features_df)

        model_path = os.path.join(self.model_dir, f"hmm_v_{version_id}.joblib")
        mapping_path = os.path.join(self.model_dir, f"mapping_v_{version_id}.json")

        joblib.dump(model, model_path)
        with open(mapping_path, "w", encoding="utf-8") as f:
            json.dump({str(k): v.value for k, v in mapping.items()}, f)

    def bootstrap_from_candles(
        self,
        candles_by_symbol: Dict[str, Iterable[dict]],
        version_id: str,
        timeframe: str,
    ) -> None:
        """
        Build a verification-only model from fresh exchange candles.

        This is deliberately intended for safe runtime verification when a
        prevalidated artifact is absent. Production/live execution must still
        provision a reviewed model artifact instead of auto-training one.
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
                snapshot = engine.compute_features(
                    symbol,
                    timeframe,
                    candle_list[:end],
                )
                rows.append(snapshot.features)

        if len(rows) < 50:
            raise ValueError(
                f"Insufficient feature history to bootstrap HMM: {len(rows)} samples"
            )

        features_df = pd.DataFrame(rows).dropna()
        self.train_and_save(features_df, version_id)

    def _map_states_to_regimes(self, df: pd.DataFrame) -> Dict[int, MarketRegime]:
        """Analyzes state statistics to map arbitrary HMM integers to domain regimes."""
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
    ) -> Tuple[hmm.GaussianHMM, Dict[int, MarketRegime]]:
        """Loads a specific version of the model and its mapping."""
        model_path = os.path.join(self.model_dir, f"hmm_v_{version_id}.joblib")
        mapping_path = os.path.join(self.model_dir, f"mapping_v_{version_id}.json")

        if not os.path.exists(model_path) or not os.path.exists(mapping_path):
            raise FileNotFoundError(f"Model version {version_id} missing files.")

        model = joblib.load(model_path)
        with open(mapping_path, "r", encoding="utf-8") as f:
            raw_map = json.load(f)

        mapping = {int(k): MarketRegime(v) for k, v in raw_map.items()}
        return model, mapping
