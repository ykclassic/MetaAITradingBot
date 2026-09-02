"""Feature engineering for the trading pipeline."""

from datetime import datetime, timezone
from typing import List

import pandas as pd

from app.domain.models import FeatureSnapshot
from app.features.indicators import (
    calculate_atr,
    calculate_bollinger_bands_width,
    calculate_ema,
    calculate_rsi,
)


class PandasFeatureEngine:
    """Deterministic pandas implementation of the feature-engine contract."""

    FEATURE_VERSION = "1.0.0"
    REQUIRED_COLUMNS = ("time", "open", "high", "low", "close", "tick_volume")
    MIN_CANDLES = 50

    def compute_features(
        self, symbol: str, timeframe: str, candles: List[dict]
    ) -> FeatureSnapshot:
        if len(candles) < self.MIN_CANDLES:
            raise ValueError(
                f"Insufficient data: need at least {self.MIN_CANDLES} candles, got {len(candles)}"
            )

        missing = [key for key in self.REQUIRED_COLUMNS if key not in candles[0]]
        if missing:
            raise ValueError(f"Candle data missing '{missing[0]}'")

        frame = pd.DataFrame(candles)
        frame = frame.sort_values("time").reset_index(drop=True)
        for column in ("open", "high", "low", "close", "tick_volume"):
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

        if frame[list(self.REQUIRED_COLUMNS)].isna().any().any():
            raise ValueError("Candle data contains invalid numeric values")

        close = frame["close"]
        ema20 = calculate_ema(close, 20)
        ema50 = calculate_ema(close, 50)
        rsi = calculate_rsi(close, 14)
        atr = calculate_atr(frame["high"], frame["low"], close, 14)
        bb_width = calculate_bollinger_bands_width(close, 20)

        latest = {
            "close": float(close.iloc[-1]),
            "ema_20": float(ema20.iloc[-1]),
            "ema_50": float(ema50.iloc[-1]),
            "rsi_14": float(rsi.iloc[-1]),
            "atr_14": float(atr.iloc[-1]),
            "bb_width_20": float(bb_width.iloc[-1]),
        }
        latest["trend_distance"] = float(
            (latest["ema_20"] - latest["ema_50"]) / latest["close"]
        )

        if any(pd.isna(value) for value in latest.values()):
            raise ValueError("Insufficient data to calculate complete feature set")

        timestamp = datetime.fromtimestamp(float(frame["time"].iloc[-1]), tz=timezone.utc)
        return FeatureSnapshot(
            timestamp=timestamp,
            symbol=symbol,
            timeframe=timeframe,
            features=latest,
            feature_version=self.FEATURE_VERSION,
        )
