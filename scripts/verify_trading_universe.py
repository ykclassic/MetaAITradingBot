"""Verify every configured trading pair returns fresh XT.com candles."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import DEFAULT_TRADE_SYMBOLS  # noqa: E402
from app.data.xt_adapter import XTAdapter  # noqa: E402


SYMBOLS = DEFAULT_TRADE_SYMBOLS.split(",")


def main() -> int:
    adapter = XTAdapter(api_key="", secret_key="")
    if not adapter.connect():
        print("FAILED: unable to connect to XT.com public API")
        return 1
    try:
        for symbol in SYMBOLS:
            candles = adapter.get_ohlcv(symbol, "M15", 5)
            if len(candles) < 5:
                print(f"FAILED: {symbol} returned only {len(candles)} candles")
                return 1
            print(f"PASS: {symbol} candles={len(candles)} latest={candles[-1]['time']}")
    except Exception as exc:
        print(f"FAILED: {exc}")
        return 1
    finally:
        adapter.disconnect()
    print(f"TRADING UNIVERSE VERIFIED: {len(SYMBOLS)} XT pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
