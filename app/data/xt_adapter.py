"""
XT.com Implementation of the MarketDataAdapter Protocol.
Interacts with the XT.com REST API for market data and order execution.
"""

import hmac
import hashlib
import time
import requests
import logging
from datetime import datetime, timezone
from typing import List, Optional

from app.core.interfaces import MarketDataAdapter
from app.domain.models import AccountState, OrderRequest, OrderResult, Position
from app.domain.enums import ConnectionState, SignalDirection, OrderExecutionState

logger = logging.getLogger(__name__)

class XTAdapter(MarketDataAdapter):
    BASE_URL = "https://sapi.xt.com"

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self._state = ConnectionState.DISCONNECTED
        self.session = requests.Session()

    def _generate_signature(self, query_string: str, timestamp: str) -> str:
        """Generates HMAC SHA256 signature required by XT.com API."""
        payload = f"{query_string}#{timestamp}"
        return hmac.new(
            self.secret_key.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _get_headers(self, query_string: str = "") -> dict:
        timestamp = str(int(time.time() * 1000))
        return {
            "validate-appkey": self.api_key,
            "validate-timestamp": timestamp,
            "validate-signature": self._generate_signature(query_string, timestamp),
            "Content-Type": "application/json"
        }

    def connect(self) -> bool:
        """Validates connection by hitting a public XT.com endpoint."""
        self._state = ConnectionState.CONNECTING
        try:
            response = self.session.get(f"{self.BASE_URL}/v4/public/time", timeout=5)
            response.raise_for_status()
            self._state = ConnectionState.CONNECTED
            logger.info("Successfully connected to XT.com API.")
            return True
        except requests.RequestException as e:
            logger.error(f"XT.com connection failed: {e}")
            self._state = ConnectionState.DISCONNECTED
            return False

    def disconnect(self) -> None:
        self.session.close()
        self._state = ConnectionState.DISCONNECTED
        logger.info("Disconnected from XT.com.")

    def is_connected(self) -> bool:
        return self._state == ConnectionState.CONNECTED

    def get_account_state(self) -> AccountState:
        """Fetches wallet balances from XT.com and maps to Domain AccountState."""
        if not self.is_connected():
            raise ConnectionError("XT.com is not connected.")

        try:
            response = self.session.get(
                f"{self.BASE_URL}/v4/balances", 
                headers=self._get_headers(),
                timeout=5
            )
            response.raise_for_status()
            data = response.json().get("result", {})
            
            # Simplified aggregation: assuming a unified USDT margin balance for quant trading
            usdt_asset = next((asset for asset in data.get("assets", []) if asset["currency"] == "usdt"), None)
            balance = float(usdt_asset["availableAmount"]) if usdt_asset else 0.0
            
            positions = self.get_open_positions()

            return AccountState(
                balance=balance,
                equity=balance, # Simplified unless tracking unrealized PnL via websockets
                margin=0.0,
                free_margin=balance,
                daily_start_equity=balance,
                current_daily_drawdown_pct=0.0,
                open_positions_count=len(positions)
            )
        except Exception as e:
            self._state = ConnectionState.DEGRADED
            raise RuntimeError(f"Failed to retrieve account info from XT.com: {e}")

    def get_ohlcv(self, symbol: str, timeframe: str, count: int) -> List[dict]:
        """Fetches historical klines from XT.com."""
        interval_map = {"M1": "1m", "M5": "5m", "M15": "15m", "H1": "1h", "D1": "1d"}
        xt_interval = interval_map.get(timeframe)
        
        if not xt_interval:
            raise ValueError(f"Unsupported timeframe mapping for XT.com: {timeframe}")

        # XT.com requires symbols in lowercase underscore format (e.g., btc_usdt)
        xt_symbol = symbol.lower().replace("/", "_")
        
        try:
            params = {"symbol": xt_symbol, "interval": xt_interval, "limit": count}
            response = self.session.get(
                f"{self.BASE_URL}/v4/public/kline", 
                params=params,
                timeout=5
            )
            response.raise_for_status()
            data = response.json().get("result", [])
            
            # Map XT.com standard array [t, o, c, h, l, v, ...] to Domain Dict
            return [{
                "time": int(kline[0]) / 1000, # Convert ms to s
                "open": float(kline[1]),
                "close": float(kline[2]),
                "high": float(kline[3]),
                "low": float(kline[4]),
                "tick_volume": float(kline[5])
            } for kline in data]
            
        except Exception as e:
            raise ValueError(f"Error fetching OHLCV from XT.com for {symbol}: {e}")

    def send_order(self, request: OrderRequest) -> OrderResult:
        """Translates and submits the order to XT.com."""
        if not self.is_connected():
            return self._build_failed_result(request, OrderExecutionState.REJECTED_BY_BROKER, "XT.com Disconnected")

        xt_symbol = request.symbol.lower().replace("/", "_")
        side = "BUY" if request.direction == SignalDirection.BUY else "SELL"
        
        payload = {
            "symbol": xt_symbol,
            "clientOrderId": request.idempotency_key[:32], # XT.com limits client order ID length
            "side": side,
            "type": "LIMIT",
            "timeInForce": "GTC",
            "price": str(request.price),
            "quantity": str(request.volume)
        }

        try:
            # Note: query_string for POST body requires URL encoded payload logic in production
            response = self.session.post(
                f"{self.BASE_URL}/v4/order",
                json=payload,
                headers=self._get_headers(str(payload)),
                timeout=5
            )
            data = response.json()
            
            if data.get("rc") == 0:
                result = data.get("result", {})
                return OrderResult(
                    idempotency_key=request.idempotency_key,
                    correlation_id=request.correlation_id,
                    mt5_ticket=result.get("orderId"), # Repurposing mt5_ticket field for universal order_id
                    execution_state=OrderExecutionState.FILLED,
                    fill_price=request.price,
                    filled_volume=request.volume,
                    executed_at=datetime.now(timezone.utc)
                )
            else:
                return self._build_failed_result(
                    request, OrderExecutionState.REJECTED_BY_BROKER, f"XT.com Error: {data.get('mc')}"
                )

        except Exception as e:
            self._state = ConnectionState.DEGRADED
            return self._build_failed_result(request, OrderExecutionState.EXECUTION_UNCERTAIN, str(e))

    def get_open_positions(self) -> List[Position]:
        # Implementation for XT.com open orders/positions query
        return []

    def _build_failed_result(self, request: OrderRequest, state: OrderExecutionState, msg: str) -> OrderResult:
        return OrderResult(
            idempotency_key=request.idempotency_key,
            correlation_id=request.correlation_id,
            mt5_ticket=None,
            execution_state=state,
            fill_price=0.0,
            filled_volume=0.0,
            executed_at=datetime.now(timezone.utc),
            error_message=msg
        )