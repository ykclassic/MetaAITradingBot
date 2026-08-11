"""
Low-level MetaTrader 5 API Wrapper.
Isolates the external MetaTrader5 package dependency and provides safe, exception-caught execution.
"""

import MetaTrader5 as mt5
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class MT5Client:
    """Safe wrapper around the MetaTrader5 library."""

    @staticmethod
    def initialize(path: Optional[str] = None, login: Optional[int] = None, 
                   password: Optional[str] = None, server: Optional[str] = None) -> bool:
        try:
            if login and password and server:
                return mt5.initialize(path=path, login=login, password=password, server=server)
            return mt5.initialize(path=path)
        except Exception as e:
            logger.error(f"MT5 initialization crashed: {e}")
            return False

    @staticmethod
    def shutdown() -> None:
        mt5.shutdown()

    @staticmethod
    def terminal_info() -> Optional[Dict[str, Any]]:
        info = mt5.terminal_info()
        return info._asdict() if info else None

    @staticmethod
    def account_info() -> Optional[Dict[str, Any]]:
        info = mt5.account_info()
        return info._asdict() if info else None

    @staticmethod
    def symbol_info(symbol: str) -> Optional[Dict[str, Any]]:
        info = mt5.symbol_info(symbol)
        return info._asdict() if info else None

    @staticmethod
    def copy_rates_from_pos(symbol: str, timeframe: int, start_pos: int, count: int) -> Optional[List[Dict[str, Any]]]:
        rates = mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count)
        if rates is None or len(rates) == 0:
            return None
        # Convert numpy structured array to list of dicts for domain consumption
        return [{name: float(rate[name]) if name in ['open', 'high', 'low', 'close', 'tick_volume'] else rate[name] 
                 for name in rates.dtype.names} for rate in rates]

    @staticmethod
    def positions_get() -> Optional[List[Dict[str, Any]]]:
        positions = mt5.positions_get()
        if positions is None:
            return None
        return [pos._asdict() for pos in positions]

    @staticmethod
    def order_send(request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = mt5.order_send(request)
        return result._asdict() if result else None