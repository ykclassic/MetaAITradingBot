"""
Evaluates registered strategies and resolves signal conflicts.
Promotes a single winning Signal per evaluation cycle.
"""

import logging
from typing import List, Optional

from app.core.interfaces import StrategyProtocol, StrategySelectorProtocol
from app.domain.models import FeatureSnapshot, RegimeResult, Signal
from app.domain.enums import SignalDirection

logger = logging.getLogger(__name__)


class ConfidenceBasedSelector(StrategySelectorProtocol):
    """
    Selects the highest confidence signal. 
    Cancels all signals if conflicting directions are detected.
    """
    
    def __init__(self, strategies: List[StrategyProtocol]):
        if not strategies:
            raise ValueError("Selector requires at least one registered strategy.")
        self.strategies = strategies

    def evaluate(self, features: FeatureSnapshot, regime: RegimeResult) -> Optional[Signal]:
        generated_signals: List[Signal] = []

        # 1. Aggregate signals from all strategies
        for strategy in self.strategies:
            try:
                signal = strategy.generate_signal(features, regime)
                if signal:
                    generated_signals.append(signal)
            except Exception as e:
                # Log strategy failure but do not crash the entire evaluation cycle
                logger.error(f"Strategy {getattr(strategy, 'name', 'Unknown')} crashed during evaluation: {e}")

        if not generated_signals:
            return None

        # 2. Conflict Resolution
        directions = {s.direction for s in generated_signals}
        if len(directions) > 1:
            logger.warning(
                f"Conflicting signals detected for {features.symbol}. "
                f"Count: {len(generated_signals)}. Discarding all signals for safety."
            )
            return None

        # 3. Conviction Ranking
        # Sort signals by confidence in descending order
        generated_signals.sort(key=lambda s: s.signal_confidence, reverse=True)
        
        winning_signal = generated_signals[0]
        
        logger.info(
            f"Selected Signal: {winning_signal.strategy_name} "
            f"Direction: {winning_signal.direction.name} "
            f"Confidence: {winning_signal.signal_confidence}"
        )
        
        return winning_signal