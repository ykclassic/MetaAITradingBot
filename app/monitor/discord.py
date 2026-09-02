"""Discord webhook based operational monitor.

The webhook identifies the dedicated Discord channel. The bot never stores or
logs the webhook URL; it is supplied through an environment variable/secret.
"""

from __future__ import annotations

import logging
import threading
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

import requests

logger = logging.getLogger(__name__)


class DiscordSystemMonitor:
    """Send structured bot lifecycle and trading-cycle telemetry to Discord."""

    def __init__(self, webhook_url: str, timeout: float = 5.0, enabled: Optional[bool] = None):
        self.webhook_url = webhook_url.strip()
        self.timeout = timeout
        self.enabled = bool(self.webhook_url) if enabled is None else enabled
        self._lock = threading.Lock()

    def _send(self, title: str, description: str, level: str = "INFO", fields: Optional[Dict[str, Any]] = None) -> None:
        if not self.enabled or not self.webhook_url:
            return
        payload = {
            "username": "MetaAI Trading Bot",
            "embeds": [{
                "title": title[:256],
                "description": description[:4096],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "fields": [
                    {"name": str(k)[:256], "value": str(v)[:1024], "inline": True}
                    for k, v in (fields or {}).items()
                ],
                "footer": {"text": f"MetaAI Trading Bot • {level}"},
            }],
        }
        try:
            with self._lock:
                response = requests.post(self.webhook_url, json=payload, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            # Monitoring must never stop the trading process.
            logger.warning("Discord monitoring delivery failed: %s", exc)

    def startup(self, symbols: Iterable[str], timeframe: str, live_trading_enabled: bool) -> None:
        self._send(
            "🟢 BOT STARTED",
            "Trading pipeline initialized.",
            fields={
                "Symbols": ", ".join(symbols),
                "Timeframe": timeframe,
                "Live trading": live_trading_enabled,
                "Mode": "LIVE" if live_trading_enabled else "SAFE / DRY-RUN",
            },
        )

    def cycle_started(self, symbols: Iterable[str], timeframe: str) -> None:
        self._send(
            "🔄 TRADING CYCLE START",
            "A complete market-data → features → regime → signal → risk → execution-gate cycle has started.",
            fields={"Symbols": ", ".join(symbols), "Timeframe": timeframe},
        )

    def account_state(self, account: Any) -> None:
        self._send(
            "💰 ACCOUNT STATE",
            "Authenticated account snapshot received from XT.com.",
            fields={
                "Equity": account.equity,
                "Available": account.free_margin,
                "Open orders": account.open_positions_count,
                "Daily drawdown %": account.current_daily_drawdown_pct,
            },
        )

    def symbol_update(self, symbol: str, status: str, **details: Any) -> None:
        self._send(
            f"📊 {symbol} — {status}",
            "Symbol processing update.",
            fields=details,
        )

    def cycle_completed(self, processed: int, signals: int, approved: int, executions: int, duration_seconds: float) -> None:
        self._send(
            "✅ TRADING CYCLE COMPLETE",
            "Trading cycle completed successfully.",
            fields={
                "Symbols processed": processed,
                "Signals": signals,
                "Risk approved": approved,
                "Execution attempts": executions,
                "Duration (s)": round(duration_seconds, 3),
            },
        )

    def error(self, title: str, message: str, critical: bool = False) -> None:
        self._send(
            ("🚨 " if critical else "⚠️ ") + title,
            message,
            level="CRITICAL" if critical else "WARNING",
        )

    def shutdown(self, reason: str = "normal") -> None:
        self._send("🔴 BOT STOPPED", "Trading pipeline stopped.", fields={"Reason": reason})
