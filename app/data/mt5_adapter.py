"""
MT5 Implementation of the MarketDataAdapter Protocol.
Manages the connection state machine and translates MT5 data to Domain Models.
"""

import MetaTrader5 as mt5
import logging
import time
from datetime import datetime, timezone
from typing import List, Optional

from app.core.interfaces import MarketDataAdapter
from app.data.mt5_client import MT5Client
from app.domain.models import AccountState, OrderRequest, OrderResult, Position
from app.domain.enums import ConnectionState, SignalDirection, OrderExecutionState

logger = logging.getLogger(__name__)


class MT5Adapter(MarketDataAdapter):
    def __init__(self, login: int, password: str, server: str, path: str = ""):
        self.login = login
        self.password = password
        self.server = server
        self.path = path
        self._state = ConnectionState.DISCONNECTED

    def connect(self) -> bool:
        """Initializes connection and logs into the MT5 terminal."""
        self._set_state(ConnectionState.CONNECTING)
        
        initialized = MT5Client.initialize(
            path=self.path,
            login=self.login,
            password=self.password,
            server=self.server
        )
        
        if not initialized:
            logger.error("Failed to initialize MT5 connection.")
            self._set_state(ConnectionState.DISCONNECTED)
            return False

        # Validate connection by fetching terminal info
        t_info = MT5Client.terminal_info()
        if t_info and t_info.get("connected"):
            self._set_state(ConnectionState.CONNECTED)
            logger.info("Successfully connected to MT5.")
            return True
        
        self._set_state(ConnectionState.DISCONNECTED)
        return False

    def disconnect(self) -> None:
        """Gracefully disconnects from MT5."""
        MT5Client.shutdown()
        self._set_state(ConnectionState.DISCONNECTED)
        logger.info("Disconnected from MT5.")

    def is_connected(self) -> bool:
        """Performs a health check and updates the state machine."""
        if self._state == ConnectionState.DISCONNECTED:
            return False

        t_info = MT5Client.terminal_info()
        if not t_info or not t_info.get("connected"):
            logger.warning("MT5 connection lost.")
            self._set_state(ConnectionState.DEGRADED)
            return False
            
        self._set_state(ConnectionState.CONNECTED)
        return True

    def _set_state(self, state: ConnectionState) -> None:
        if self._state != state:
            logger.info(f"Connection state transitioned: {self._state.value} -> {state.value}")
            self._state = state

    def get_account_state(self) -> AccountState:
        """Retrieves and maps MT5 account info to Domain AccountState."""
        if not self.is_connected():
            raise ConnectionError("Cannot fetch account state: MT5 is not connected.")

        acc = MT5Client.account_info()
        if not acc:
            self._set_state(ConnectionState.DEGRADED)
            raise RuntimeError("Failed to retrieve account info from MT5.")

        positions = self.get_open_positions()

        return AccountState(
            balance=acc.get("balance", 0.0),
            equity=acc.get("equity", 0.0),
            margin=acc.get("margin", 0.0),
            free_margin=acc.get("margin_free", 0.0),
            daily_start_equity=acc.get("balance", 0.0),  # Simplified for now; usually requires DB tracking
            current_daily_drawdown_pct=0.0,              # Calculated downstream by Risk Manager
            open_positions_count=len(positions)
        )

    def get_ohlcv(self, symbol: str, timeframe: str, count: int) -> List[dict]:
        """Fetches historical rates."""
        if not self.is_connected():
            raise ConnectionError("Cannot fetch OHLCV: MT5 is not connected.")

        tf_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "H1": mt5.TIMEFRAME_H1,
            "D1": mt5.TIMEFRAME_D1,
        }
        
        mt5_tf = tf_map.get(timeframe)
        if not mt5_tf:
            raise ValueError(f"Unsupported timeframe mapping: {timeframe}")

        rates = MT5Client.copy_rates_from_pos(symbol, mt5_tf, 0, count)
        if not rates:
            raise ValueError(f"No rates returned for {symbol} at {timeframe}")
        
        return rates

    def send_order(self, request: OrderRequest) -> OrderResult:
        """Submits an order to MT5 and handles the response deterministically."""
        if not self.is_connected():
            return OrderResult(
                idempotency_key=request.idempotency_key,
                correlation_id=request.correlation_id,
                mt5_ticket=None,
                execution_state=OrderExecutionState.REJECTED_BY_BROKER,
                fill_price=0.0,
                filled_volume=0.0,
                executed_at=datetime.now(timezone.utc),
                error_message="MT5 Disconnected"
            )

        order_type = mt5.ORDER_TYPE_BUY if request.direction == SignalDirection.BUY else mt5.ORDER_TYPE_SELL
        
        # Note: MT5 comment field is limited to 31 chars.
        # If idempotency_key is a UUID, we slice it or map it. For now, slice.
        comment_key = request.idempotency_key[:31]

        mt5_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": request.symbol,
            "volume": request.volume,
            "type": order_type,
            "price": request.price,
            "sl": request.stop_loss,
            "tp": request.take_profit,
            "deviation": request.slippage_tolerance,
            "magic": request.magic_number,
            "comment": comment_key,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = MT5Client.order_send(mt5_request)

        if not result:
            self._set_state(ConnectionState.DEGRADED)
            return OrderResult(
                idempotency_key=request.idempotency_key,
                correlation_id=request.correlation_id,
                mt5_ticket=None,
                execution_state=OrderExecutionState.EXECUTION_UNCERTAIN,
                fill_price=0.0,
                filled_volume=0.0,
                executed_at=datetime.now(timezone.utc),
                error_message="Null response from MT5 API. Execution uncertain."
            )

        # Parse MT5 Result Code (10009 is TRADE_RETCODE_DONE)
        retcode = result.get("retcode")
        if retcode == mt5.TRADE_RETCODE_DONE:
            return OrderResult(
                idempotency_key=request.idempotency_key,
                correlation_id=request.correlation_id,
                mt5_ticket=result.get("order"),
                execution_state=OrderExecutionState.FILLED,
                fill_price=result.get("price", 0.0),
                filled_volume=result.get("volume", 0.0),
                executed_at=datetime.now(timezone.utc)
            )
        
        return OrderResult(
            idempotency_key=request.idempotency_key,
            correlation_id=request.correlation_id,
            mt5_ticket=result.get("order"),
            execution_state=OrderExecutionState.REJECTED_BY_BROKER,
            fill_price=0.0,
            filled_volume=0.0,
            executed_at=datetime.now(timezone.utc),
            error_message=result.get("comment", f"Broker rejection code: {retcode}")
        )

    def get_open_positions(self) -> List[Position]:
        """Retrieves open positions and maps them to Domain models."""
        if not self.is_connected():
            return []

        raw_positions = MT5Client.positions_get()
        if raw_positions is None:
            return []

        positions = []
        for p in raw_positions:
            direction = SignalDirection.BUY if p["type"] == mt5.POSITION_TYPE_BUY else SignalDirection.SELL
            positions.append(Position(
                position_id=p["ticket"],
                correlation_id=None, # In a real scenario, map this via DB lookup using ticket or magic
                symbol=p["symbol"],
                direction=direction,
                volume=p["volume"],
                open_price=p["price_open"],
                stop_loss=p["sl"],
                take_profit=p["tp"],
                opened_at=datetime.fromtimestamp(p["time"], timezone.utc),
                magic_number=p["magic"]
            ))
        return positions