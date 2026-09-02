"""Print current trading-journal metrics as JSON or human-readable output."""

import argparse
import json

from app.config import AppConfig
from app.persistence.database import SQLiteManager
from app.performance.tracker import PerformanceTracker


def main() -> None:
    parser = argparse.ArgumentParser(description="Report MetaAI trading performance metrics.")
    parser.add_argument("--db", default=None, help="SQLite journal path (defaults to PERFORMANCE_DB_PATH).")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    config = AppConfig.load_from_env()
    db = SQLiteManager(args.db or config.performance_db_path)
    tracker = PerformanceTracker(db)
    metrics = tracker.get_metrics()

    if args.json:
        print(json.dumps(metrics.to_dict(), indent=2, sort_keys=True, allow_nan=False))
        return

    for key, value in metrics.to_dict().items():
        if isinstance(value, float):
            print(f"{key}: {value:.6f}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
