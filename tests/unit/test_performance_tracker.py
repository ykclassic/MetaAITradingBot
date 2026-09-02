from app.persistence.database import SQLiteManager
from app.performance.tracker import PerformanceTracker


def test_performance_metrics_from_closed_trades():
    db = SQLiteManager(":memory:")
    tracker = PerformanceTracker(db)
    tracker.record_event("TRADE_CLOSED", pnl=100.0, r_multiple=2.0, details={"holding_seconds": 60})
    tracker.record_event("TRADE_CLOSED", pnl=-50.0, r_multiple=-1.0, details={"holding_seconds": 120})
    tracker.record_event("TRADE_CLOSED", pnl=25.0, r_multiple=0.5, details={"holding_seconds": 90})

    metrics = tracker.get_metrics()
    assert metrics.total_trades == 3
    assert metrics.winning_trades == 2
    assert metrics.losing_trades == 1
    assert metrics.win_rate_pct == 100 * 2 / 3
    assert metrics.net_pnl == 75.0
    assert metrics.gross_profit == 125.0
    assert metrics.gross_loss == 50.0
    assert metrics.profit_factor == 2.5
    assert metrics.expectancy == 25.0
    assert metrics.average_r_multiple == 0.5
    assert metrics.max_drawdown == 50.0
    assert metrics.average_holding_seconds == 90.0


def test_profit_factor_is_json_safe_without_losses():
    db = SQLiteManager(":memory:")
    tracker = PerformanceTracker(db)
    tracker.record_event("TRADE_CLOSED", pnl=100.0, r_multiple=1.0, details={})
    assert tracker.get_metrics().profit_factor is None
