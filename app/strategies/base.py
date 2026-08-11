"""
Abstract Base Strategy.
Provides boilerplate for regime filtering and Signal construction.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime, timedelta

from app.core.interfaces import StrategyProtocol
from app.domain.models import FeatureSnapshot, RegimeResult, Signal
from app.domain.enums import MarketRegime, SignalDirection


class BaseStrategy(ABC, StrategyProtocol):
    """Abstract implementation of the StrategyProtocol."""
    
    def __init__(self):
        # Enforce that subclasses define these attributes
        assert hasattr(self, 'name'), "Strategy must define a 'name'"
        assert hasattr(self, 'version'), "Strategy must define a 'version'"
        assert hasattr(self, 'supported_regimes'), "Strategy must define 'supported_regimes'"
        assert hasattr(self, 'required_features'), "Strategy must define 'required_features'"

    def generate_signal(self, features: FeatureSnapshot, regime: RegimeResult) -> Optional[Signal]:
        """Validates inputs before delegating to the specific strategy logic."""
        if regime.regime not in self.supported_regimes:
            return None

        for req in self.required_features:
            if req not in features.features:
                raise ValueError(f"Strategy {self.name} missing required feature: {req}")

        return self._evaluate_logic(features, regime)

    @abstractmethod
    def _evaluate_logic(self, features: FeatureSnapshot, regime: RegimeResult) -> Optional[Signal]:
        """Core logic to be implemented by child classes."""
        pass

    def _create_signal(self, 
                       features: FeatureSnapshot, 
                       direction: SignalDirection, 
                       entry_price: float, 
                       stop_loss: float, 
                       take_profit: float, 
                       confidence: float, 
                       expiration_minutes: int = 15) -> Signal:
        """Helper to construct a uniform Signal object."""
        return Signal(
            symbol=features.symbol,
            timeframe=features.timeframe,
            direction=direction,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            strategy_name=self.name,
            strategy_version=self.version,
            signal_confidence=confidence,
            expiration=datetime.utcnow() + timedelta(minutes=expiration_minutes)
        )