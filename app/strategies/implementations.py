"""
Specific Strategy Implementations.
Each strategy applies explicit entry, SL, and TP rules based on deterministic features.
"""

from typing import Optional
from app.strategies.base import BaseStrategy
from app.domain.models import FeatureSnapshot, RegimeResult, Signal
from app.domain.enums import MarketRegime, SignalDirection


class EMATrendStrategy(BaseStrategy):
    name = "EMA_Trend"
    version = "1.0.0"
    supported_regimes = [MarketRegime.STRONG_TREND_UP, MarketRegime.STRONG_TREND_DOWN]
    required_features = ["ema_20", "ema_50", "rsi_14", "atr_14", "close"]

    def _evaluate_logic(self, features: FeatureSnapshot, regime: RegimeResult) -> Optional[Signal]:
        f = features.features
        close, ema20, ema50, rsi, atr = f["close"], f["ema_20"], f["ema_50"], f["rsi_14"], f["atr_14"]

        # BUY Logic: Trend is UP, price pulled back near EMA20, RSI is not overbought
        if regime.regime == MarketRegime.STRONG_TREND_UP:
            if close > ema50 and (ema20 * 0.999) < close < (ema20 * 1.002) and rsi < 65.0:
                return self._create_signal(
                    features=features,
                    direction=SignalDirection.BUY,
                    entry_price=close,
                    stop_loss=close - (1.5 * atr),
                    take_profit=close + (3.0 * atr),
                    confidence=0.80,
                    expiration_minutes=15
                )

        # SELL Logic: Trend is DOWN, price pulled back near EMA20, RSI is not oversold
        elif regime.regime == MarketRegime.STRONG_TREND_DOWN:
            if close < ema50 and (ema20 * 0.998) < close < (ema20 * 1.001) and rsi > 35.0:
                return self._create_signal(
                    features=features,
                    direction=SignalDirection.SELL,
                    entry_price=close,
                    stop_loss=close + (1.5 * atr),
                    take_profit=close - (3.0 * atr),
                    confidence=0.80,
                    expiration_minutes=15
                )
        
        return None


class RSIMeanReversionStrategy(BaseStrategy):
    name = "RSI_MeanReversion"
    version = "1.0.0"
    supported_regimes = [MarketRegime.RANGE_LOW_VOL, MarketRegime.RANGE_HIGH_VOL]
    required_features = ["rsi_14", "atr_14", "close"]

    def _evaluate_logic(self, features: FeatureSnapshot, regime: RegimeResult) -> Optional[Signal]:
        f = features.features
        close, rsi, atr = f["close"], f["rsi_14"], f["atr_14"]

        # Adjust thresholds based on volatility
        oversold_threshold = 30.0 if regime.regime == MarketRegime.RANGE_LOW_VOL else 25.0
        overbought_threshold = 70.0 if regime.regime == MarketRegime.RANGE_LOW_VOL else 75.0
        tp_multiplier = 1.5 if regime.regime == MarketRegime.RANGE_LOW_VOL else 2.0

        if rsi < oversold_threshold:
            return self._create_signal(
                features=features,
                direction=SignalDirection.BUY,
                entry_price=close,
                stop_loss=close - (1.0 * atr),
                take_profit=close + (tp_multiplier * atr),
                confidence=0.75,
                expiration_minutes=30
            )
            
        elif rsi > overbought_threshold:
            return self._create_signal(
                features=features,
                direction=SignalDirection.SELL,
                entry_price=close,
                stop_loss=close + (1.0 * atr),
                take_profit=close - (tp_multiplier * atr),
                confidence=0.75,
                expiration_minutes=30
            )

        return None


class ATRBreakoutStrategy(BaseStrategy):
    name = "ATR_Breakout"
    version = "1.0.0"
    # Breakouts happen best transitioning out of low volatility, or continuing high vol
    supported_regimes = [MarketRegime.RANGE_LOW_VOL, MarketRegime.STRONG_TREND_UP, MarketRegime.STRONG_TREND_DOWN]
    required_features = ["atr_14", "bb_width_20", "close", "ema_20"]

    def _evaluate_logic(self, features: FeatureSnapshot, regime: RegimeResult) -> Optional[Signal]:
        f = features.features
        close, ema20, atr, bb_width = f["close"], f["ema_20"], f["atr_14"], f["bb_width_20"]

        # We look for a squeeze condition using bb_width
        if bb_width < 0.002: # Highly compressed
            if close > ema20 + (0.5 * atr):
                return self._create_signal(
                    features=features,
                    direction=SignalDirection.BUY,
                    entry_price=close,
                    stop_loss=close - (2.0 * atr),
                    take_profit=close + (4.0 * atr),
                    confidence=0.70,
                    expiration_minutes=60
                )
            elif close < ema20 - (0.5 * atr):
                return self._create_signal(
                    features=features,
                    direction=SignalDirection.SELL,
                    entry_price=close,
                    stop_loss=close + (2.0 * atr),
                    take_profit=close - (4.0 * atr),
                    confidence=0.70,
                    expiration_minutes=60
                )
                
        return None