"""
Signal selection and conflict resolution.
"""

import logging
from typing import List, Optional

from app.core.interfaces import StrategyProtocol, StrategySelectorProtocol
from app.domain.models import FeatureSnapshot, RegimeResult, Signal

logger = logging.getLogger(__name__)


class ConfidenceBasedSelector(StrategySelectorProtocol):
    """Generate signals from registered strategies and select the strongest one."""

    def __init__(self, strategies: List[StrategyProtocol]):
        if not strategies:
            raise ValueError("Selector requires at least one registered strategy.")
        self.strategies = strategies

    def evaluate(self, features: FeatureSnapshot, regime: RegimeResult) -> Optional[Signal]:
        generated_signals: List[Signal] = []

        for strategy in self.strategies:
            try:
                signal = strategy.generate_signal(features, regime)
                if signal:
                    generated_signals.append(signal)
            except Exception as exc:
                logger.error(
                    "Strategy %s crashed during evaluation: %s",
                    getattr(strategy, "name", "Unknown"),
                    exc,
                )

        if not generated_signals:
            return None

        directions = {signal.direction for signal in generated_signals}
        if len(directions) > 1:
            logger.warning(
                "Conflicting signals detected for %s; discarding all signals for safety.",
                features.symbol,
            )
            return None

        return max(generated_signals, key=lambda signal: signal.signal_confidence)


class PrioritySignalSelector:
    """Compatibility selector used by the composition root and trading pipeline.

    The current policy is deterministic: reject conflicting directions and otherwise
    select the highest-confidence signal.
    """

    def select_best_signal(self, signals: List[Signal]) -> Optional[Signal]:
        if not signals:
            return None

        directions = {signal.direction for signal in signals}
        if len(directions) > 1:
            logger.warning("Conflicting signal directions detected; rejecting the cycle.")
            return None

        return max(signals, key=lambda signal: signal.signal_confidence)
