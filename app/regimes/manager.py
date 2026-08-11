"""
Manages HMM model training, persistence, versioning, and state mapping.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Tuple
from hmmlearn import hmm

from app.domain.enums import MarketRegime


class ModelManager:
    def __init__(self, model_dir: str = "models/"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)

    def train_and_save(self, features_df: pd.DataFrame, version_id: str) -> None:
        """Trains the HMM and maps states to regimes based on statistical profiles."""
        # For our 4 core market states (excluding NEWS and UNKNOWN)
        n_components = 4
        model = hmm.GaussianHMM(n_components=n_components, covariance_type="full", n_iter=100)
        
        # Features used for training (must match FeatureSnapshot order)
        train_cols = ["trend_distance", "atr_14", "rsi_14", "bb_width_20"]
        X = features_df[train_cols].values
        
        model.fit(X)
        states = model.predict(X)
        features_df["state"] = states

        # Map states statistically
        mapping = self._map_states_to_regimes(features_df)

        # Save model and mapping
        model_path = os.path.join(self.model_dir, f"hmm_v_{version_id}.joblib")
        mapping_path = os.path.join(self.model_dir, f"mapping_v_{version_id}.json")
        
        joblib.dump(model, model_path)
        with open(mapping_path, "w") as f:
            json.dump({str(k): v.value for k, v in mapping.items()}, f)

    def _map_states_to_regimes(self, df: pd.DataFrame) -> Dict[int, MarketRegime]:
        """Analyzes state statistics to map arbitrary HMM integers to domain regimes."""
        stats = df.groupby("state").agg({
            "trend_distance": "mean",
            "atr_14": "mean"
        })
        
        median_vol = stats["atr_14"].median()
        mapping = {}
        
        for state in stats.index:
            mean_trend = stats.loc[state, "trend_distance"]
            mean_vol = stats.loc[state, "atr_14"]
            
            # Simple thresholding logic for mapping (can be made more sophisticated)
            if mean_trend > 0.001:
                mapping[state] = MarketRegime.STRONG_TREND_UP
            elif mean_trend < -0.001:
                mapping[state] = MarketRegime.STRONG_TREND_DOWN
            elif mean_vol > median_vol:
                mapping[state] = MarketRegime.RANGE_HIGH_VOL
            else:
                mapping[state] = MarketRegime.RANGE_LOW_VOL
                
        return mapping

    def load_model(self, version_id: str) -> Tuple[hmm.GaussianHMM, Dict[int, MarketRegime]]:
        """Loads a specific version of the model and its mapping."""
        model_path = os.path.join(self.model_dir, f"hmm_v_{version_id}.joblib")
        mapping_path = os.path.join(self.model_dir, f"mapping_v_{version_id}.json")
        
        if not os.path.exists(model_path) or not os.path.exists(mapping_path):
            raise FileNotFoundError(f"Model version {version_id} missing files.")
            
        model = joblib.load(model_path)
        with open(mapping_path, "r") as f:
            raw_map = json.load(f)
            
        mapping = {int(k): MarketRegime(v) for k, v in raw_map.items()}
        return model, mapping