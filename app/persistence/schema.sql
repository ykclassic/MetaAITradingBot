-- Initial schema definition for system state and persistence.
-- Uses strict type affinities available in SQLite.

CREATE TABLE IF NOT EXISTS signals (
    signal_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    direction TEXT NOT NULL,
    entry_price REAL NOT NULL,
    stop_loss REAL NOT NULL,
    take_profit REAL NOT NULL,
    strategy_name TEXT NOT NULL,
    strategy_version TEXT NOT NULL,
    signal_confidence REAL NOT NULL,
    expiration TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS trade_outcomes (
    correlation_id TEXT PRIMARY KEY,
    position_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    strategy_name TEXT NOT NULL,
    regime TEXT NOT NULL,
    direction TEXT NOT NULL,
    entry_price REAL NOT NULL,
    exit_price REAL NOT NULL,
    realized_pnl REAL NOT NULL,
    r_multiple REAL NOT NULL,
    holding_seconds REAL NOT NULL,
    exit_reason TEXT NOT NULL,
    closed_at TEXT NOT NULL
);

-- Indexes to speed up learning engine queries
CREATE INDEX IF NOT EXISTS idx_outcomes_strategy_regime 
ON trade_outcomes(strategy_name, regime);