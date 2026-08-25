"""XT.com implementation of the MarketDataAdapter protocol."""

import hashlib
import hmac
import json
import logging
import time
from datetime import datetime, timezone
from typing import List
from urllib.parse import urlencode

import requests

from app.core.interfaces import MarketDataAdapter
from app.domain.enums import ConnectionState, OrderExecutionState, SignalDirection
from app.domain.models import AccountState, OrderRequest, OrderResult, Position

logger = logging.getLogger(__name__)


class XTAdapter(MarketDataAdapter):
    BASE_URL = "https://sapi.xt.com"
    RECV_WINDOW_MS = 5000

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self._state = ConnectionState.DISCONNECTED
        self.session = requests.Session()
        self._server_time_offset_ms = 0

    def _timestamp_ms(self) -> str:
        return str(int(time.time() * 1000) + self._server_time_offset_ms)

    def _signature(
        self,
        method: str,
        path: str,
        timestamp: str,
        query: str = "",
        body: str = "",
    ) -> str:
        """Generate the XT v4 HmacSHA256 canonical signature."""
        header_component = (
            "validate-algorithms=HmacSHA256"
            f"&validate-appkey={self.api_key}"
            f"&validate-recvwindow={self.RECV_WINDOW_MS}"
            f"&validate-timestamp={timestamp}"
        )
        data = query if query else body
        if data:
            signing_payload = f"{header_component}#{method.upper()}#{path}#{data}"
        else:
            signing_payload = f"{header_component}#{method.upper()}#{path}"
        return hmac.new(
            self.secret_key.encode("utf-8"),
            signing_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _signed_headers(self, method: str, path: str, query: str = "", body: str = "") -> dict:
        timestamp = self._timestamp_ms()
        return {
            "validate-algorithms": "HmacSHA256",
            "validate-appkey": self.api_key,
            "validate-recvwindow": str(self.RECV_WINDOW_MS),
            "validate-timestamp": timestamp,
            "validate-signature": self._signature(method, path, timestamp, query, body),
            "Content-Type": "application/json",
        }

    def _sync_server_time(self) -> None:
        started = int(time.time() * 1000)
        response = self.session.get(f"{self.BASE_URL}/v4/public/time", timeout=5)
        response.raise_for_status()
        ended = int(time.time() * 1000)
        payload = response.json()
        if payload.get("rc") != 0:
            raise RuntimeError(
                f"XT time endpoint returned rc={payload.get('rc')}: {payload.get('mc')}"
            )
        server_time = payload.get("result", {}).get("serverTime")
        if server_time is None:
            raise RuntimeError("XT time endpoint returned no serverTime")
        midpoint = (started + ended) // 2
        self._server_time_offset_ms = int(server_time) - midpoint

    def connect(self) -> bool:
        self._state = ConnectionState.CONNECTING
        try:
            self._sync_server_time()
            self._state = ConnectionState.CONNECTED
            logger.info("Successfully connected to XT.com API.")
            return True
        except (requests.RequestException, ValueError, RuntimeError) as exc:
            logger.error("XT.com connection failed: %s", exc)
            self._state = ConnectionState.DISCONNECTED
            return False

    def disconnect(self) -> None:
        self.session.close()
        self._state = ConnectionState.DISCONNECTED

    def is_connected(self) -> bool:
        return self._state == ConnectionState.CONNECTED

    def get_account_state(self) -> AccountState:
        if not self.is_connected():
            raise ConnectionError("XT.com is not connected.")
        if not self.api_key or not self.secret_key:
            raise RuntimeError("XT_API_KEY and XT_SECRET_KEY are required for authenticated account access.")

        path = "/v4/balances"
        query = ""
        try:
            response = self.session.get(
                f"{self.BASE_URL}{path}",
                headers=self._signed_headers("GET", path, query=query),
                timeout=5,
            )
            response.raise_for_status()
            payload = response.json()
            if payload.get("rc") != 0:
                raise RuntimeError(f"XT balances error rc={payload.get('rc')}: {payload.get('mc')}")

            data = payload.get("result", {})
            assets = data.get("assets", []) if isinstance(data, dict) else []
            usdt = next((asset for asset in assets if asset.get("currency", "").lower() == "usdt"), None)
            balance = float(usdt.get("availableAmount", 0.0)) if usdt else 0.0

            open_orders = self._get_open_orders()
            return AccountState(
                balance=balance,
                equity=balance,
                margin=0.0,
                free_margin=balance,
                daily_start_equity=balance,
                current_daily_drawdown_pct=0.0,
                open_positions_count=len(open_orders),
            )
        except Exception as exc:
            self._state = ConnectionState.DEGRADED
            raise RuntimeError(f"Failed to retrieve account info from XT.com: {exc}") from exc

    def get_ohlcv(self, symbol: str, timeframe: str, count: int) -> List[dict]:
        interval_map = {"M1": "1m", "M5": "5m", "M15": "15m", "H1": "1h", "D1": "1d"}
        xt_interval = interval_map.get(timeframe)
        if not xt_interval:
            raise ValueError(f"Unsupported timeframe mapping for XT.com: {timeframe}")

        xt_symbol = symbol.lower().replace("/", "_")
        response = self.session.get(
            f"{self.BASE_URL}/v4/public/kline",
            params={"symbol": xt_symbol, "interval": xt_interval, "limit": count},
            timeout=5,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("rc") != 0:
            raise RuntimeError(f"XT kline error rc={payload.get('rc')}: {payload.get('mc')}")
        return [
            {
                "time": int(kline[0] if isinstance(kline, list) else kline["t"]) / 1000,
                "open": float(kline[1] if isinstance(kline, list) else kline["o"]),
                "close": float(kline[2] if isinstance(kline, list) else kline["c"]),
                "high": float(kline[3] if isinstance(kline, list) else kline["h"]),
                "low": float(kline[4] if isinstance(kline, list) else kline["l"]),
                "tick_volume": float(kline[5] if isinstance(kline, list) else kline["q"]),
            }
            for kline in payload.get("result", [])
        ]

    def send_order(self, request: OrderRequest) -> OrderResult:
        if not self.is_connected():
            return self._build_failed_result(request, OrderExecutionState.REJECTED_BY_BROKER, "XT.com Disconnected")
        if not self.api_key or not self.secret_key:
            return self._build_failed_result(request, OrderExecutionState.REJECTED_BY_BROKER, "Missing XT credentials")

        path = "/v4/order"
        payload = {
            "symbol": request.symbol.lower().replace("/", "_"),
            "clientOrderId": request.idempotency_key[:32],
            "side": "BUY" if request.direction == SignalDirection.BUY else "SELL",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "price": request.price,
            "quantity": request.volume,
        }
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)

        try:
            response = self.session.post(
                f"{self.BASE_URL}{path}",
                data=body,
                headers=self._signed_headers("POST", path, body=body),
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("rc") != 0:
                return self._build_failed_result(
                    request,
                    OrderExecutionState.REJECTED_BY_BROKER,
                    f"XT.com Error: {data.get('mc')}",
                )

            order_id = data.get("result", {}).get("orderId")
            return OrderResult(
                idempotency_key=request.idempotency_key,
                correlation_id=request.correlation_id,
                mt5_ticket=int(order_id) if order_id is not None else None,
                execution_state=OrderExecutionState.IN_FLIGHT,
                fill_price=0.0,
                filled_volume=0.0,
                executed_at=datetime.now(timezone.utc),
            )
        except Exception as exc:
            self._state = ConnectionState.DEGRADED
            return self._build_failed_result(request, OrderExecutionState.EXECUTION_UNCERTAIN, str(exc))

    def _get_open_orders(self) -> List[dict]:
        path = "/v4/open-order"
        query_params = {"bizType": "SPOT"}
        query = urlencode(sorted(query_params.items()))
        response = self.session.get(
            f"{self.BASE_URL}{path}?{query}",
            headers=self._signed_headers("GET", path, query=query),
            timeout=5,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("rc") != 0:
            raise RuntimeError(f"XT open-order error rc={payload.get('rc')}: {payload.get('mc')}")
        return payload.get("result", [])

    def get_open_positions(self) -> List[Position]:
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
            error_message=msg,
        )
