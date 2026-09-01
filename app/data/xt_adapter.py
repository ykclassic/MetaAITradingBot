"""XT.com implementation of the MarketDataAdapter protocol."""

import hashlib
import hmac
import json
import logging
import time
from datetime import datetime, timezone
from typing import List, Optional
from urllib.parse import urlencode

import requests
from requests import Response

from app.core.interfaces import MarketDataAdapter
from app.domain.enums import ConnectionState, OrderExecutionState, SignalDirection
from app.domain.models import AccountState, OrderRequest, OrderResult, Position

logger = logging.getLogger(__name__)


class XTAdapter(MarketDataAdapter):
    BASE_URL = "https://sapi.xt.com"
    RECV_WINDOW_MS = 5000
    REQUEST_TIMEOUT = (3.05, 10.0)
    MAX_RETRIES = 2
    RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key.strip()
        self.secret_key = secret_key.strip()
        self._state = ConnectionState.DISCONNECTED
        self.session = requests.Session()
        self._server_time_offset_ms = 0

    def _timestamp_ms(self) -> str:
        return str(int(time.time() * 1000) + self._server_time_offset_ms)

    def _signature(self, method: str, path: str, timestamp: str, query: str = "", body: str = "") -> str:
        """Build XT v4's HmacSHA256 canonical signing message.

        XT v4 signs the algorithm, app key, recv window and timestamp headers,
        followed by method, path, query (when present) and exact request body.
        """
        header_component = (
            f"validate-algorithms=HmacSHA256"
            f"&validate-appkey={self.api_key}"
            f"&validate-recvwindow={self.RECV_WINDOW_MS}"
            f"&validate-timestamp={timestamp}"
        )
        components = [method.upper(), path]
        if query:
            components.append(query)
        if body:
            components.append(body)
        signing_payload = f"{header_component}#" + "#".join(components)
        return hmac.new(
            self.secret_key.encode("utf-8"),
            signing_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _signed_headers(self, method: str, path: str, query: str = "", body: str = "", timestamp: Optional[str] = None) -> dict:
        timestamp = timestamp or self._timestamp_ms()
        return {
            "validate-algorithms": "HmacSHA256",
            "validate-appkey": self.api_key,
            "validate-recvwindow": str(self.RECV_WINDOW_MS),
            "validate-timestamp": timestamp,
            "validate-signature": self._signature(method, path, timestamp, query, body),
            "Content-Type": "application/json",
        }

    @staticmethod
    def _response_payload(response: Response) -> dict:
        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(f"XT returned non-JSON response (HTTP {response.status_code})") from exc
        if not isinstance(payload, dict):
            raise RuntimeError("XT returned an unexpected JSON payload type")
        return payload

    def _sync_server_time(self) -> None:
        started = int(time.time() * 1000)
        response = self.session.get(f"{self.BASE_URL}/v4/public/time", timeout=self.REQUEST_TIMEOUT)
        response.raise_for_status()
        ended = int(time.time() * 1000)
        payload = self._response_payload(response)
        if payload.get("rc") != 0:
            raise RuntimeError(f"XT time endpoint returned rc={payload.get('rc')}: {payload.get('mc')}")
        server_time = payload.get("result", {}).get("serverTime")
        if server_time is None:
            raise RuntimeError("XT time endpoint returned no serverTime")
        self._server_time_offset_ms = int(server_time) - ((started + ended) // 2)

    def _request_json(self, method: str, path: str, *, query: str = "", body: str = "", authenticated: bool = False) -> dict:
        """Issue an XT request with bounded retry and clock-resync handling."""
        url = f"{self.BASE_URL}{path}"
        if query:
            url = f"{url}?{query}"

        attempts = 0
        clock_resynced = False
        while True:
            attempts += 1
            headers = self._signed_headers(method, path, query, body) if authenticated else {"Content-Type": "application/json"}
            try:
                response = self.session.request(
                    method.upper(),
                    url,
                    headers=headers,
                    data=body if body else None,
                    timeout=self.REQUEST_TIMEOUT,
                )
            except requests.RequestException:
                if attempts <= self.MAX_RETRIES:
                    time.sleep(0.25 * (2 ** (attempts - 1)))
                    continue
                raise

            if response.status_code in self.RETRYABLE_STATUS_CODES and attempts <= self.MAX_RETRIES:
                retry_after = response.headers.get("Retry-After")
                try:
                    delay = min(float(retry_after), 5.0) if retry_after else 0.25 * (2 ** (attempts - 1))
                except ValueError:
                    delay = 0.25 * (2 ** (attempts - 1))
                time.sleep(delay)
                continue

            payload = self._response_payload(response)
            message_code = payload.get("mc")
            if authenticated and message_code == "AUTH_105" and not clock_resynced:
                self._sync_server_time()
                clock_resynced = True
                continue

            response.raise_for_status()
            return payload

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
        try:
            payload = self._request_json("GET", "/v4/balances", authenticated=True)
            if payload.get("rc") != 0:
                raise RuntimeError(f"XT balances error rc={payload.get('rc')}: {payload.get('mc')}")
            data = payload.get("result", {})
            assets = data.get("assets", []) if isinstance(data, dict) else []
            usdt = next((asset for asset in assets if isinstance(asset, dict) and asset.get("currency", "").lower() == "usdt"), None)
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
        if count <= 0:
            raise ValueError("count must be greater than zero")
        interval_map = {"M1": "1m", "M5": "5m", "M15": "15m", "H1": "1h", "D1": "1d"}
        xt_interval = interval_map.get(timeframe)
        if not xt_interval:
            raise ValueError(f"Unsupported timeframe mapping for XT.com: {timeframe}")
        xt_symbol = symbol.lower().replace("/", "_")
        query = urlencode([("interval", xt_interval), ("limit", count), ("symbol", xt_symbol)])
        payload = self._request_json("GET", "/v4/public/kline", query=query)
        if payload.get("rc") != 0:
            raise RuntimeError(f"XT kline error rc={payload.get('rc')}: {payload.get('mc')}")
        result = payload.get("result", [])
        if not isinstance(result, list):
            raise RuntimeError("XT kline endpoint returned an unexpected result")
        candles = []
        for kline in result:
            try:
                candles.append({
                    "time": int(kline[0] if isinstance(kline, list) else kline["t"]) / 1000,
                    "open": float(kline[1] if isinstance(kline, list) else kline["o"]),
                    "close": float(kline[2] if isinstance(kline, list) else kline["c"]),
                    "high": float(kline[3] if isinstance(kline, list) else kline["h"]),
                    "low": float(kline[4] if isinstance(kline, list) else kline["l"]),
                    "tick_volume": float(kline[5] if isinstance(kline, list) else kline["q"]),
                })
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                raise RuntimeError("XT kline endpoint returned malformed candle data") from exc
        return candles

    def send_order(self, request: OrderRequest) -> OrderResult:
        """Submit an XT spot order and return the broker order id."""
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
            "bizType": "SPOT",
            "price": request.price,
            "quantity": request.volume,
        }
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
        logger.info("XT ORDER SUBMISSION: POST %s symbol=%s", path, payload["symbol"])

        try:
            data = self._request_json("POST", path, body=body, authenticated=True)
            if data.get("rc") != 0:
                return self._build_failed_result(request, OrderExecutionState.REJECTED_BY_BROKER, f"XT.com Error: {data.get('mc')}")
            result = data.get("result", {})
            order_id = result.get("orderId") if isinstance(result, dict) else None
            if order_id is None:
                return self._build_failed_result(request, OrderExecutionState.EXECUTION_UNCERTAIN, "XT accepted the request without returning orderId")
            logger.info("XT ORDER SUBMITTED: order_id=%s", order_id)
            return OrderResult(
                idempotency_key=request.idempotency_key,
                correlation_id=request.correlation_id,
                order_id=int(order_id),
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
        query = urlencode(sorted({"bizType": "SPOT"}.items()))
        payload = self._request_json("GET", path, query=query, authenticated=True)
        if payload.get("rc") != 0:
            raise RuntimeError(f"XT open-order error rc={payload.get('rc')}: {payload.get('mc')}")
        result = payload.get("result", [])
        return result if isinstance(result, list) else []

    def get_open_positions(self) -> List[Position]:
        return []

    def _build_failed_result(self, request: OrderRequest, state: OrderExecutionState, msg: str) -> OrderResult:
        return OrderResult(
            idempotency_key=request.idempotency_key,
            correlation_id=request.correlation_id,
            order_id=None,
            execution_state=state,
            fill_price=0.0,
            filled_volume=0.0,
            executed_at=datetime.now(timezone.utc),
            error_message=msg,
        )
