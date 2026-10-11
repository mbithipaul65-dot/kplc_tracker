-- Enable Foreign Key constraints in SQLite
PRAGMA foreign_keys = ON;

-- 1. Buyers Table: Stores contact details for buyers
CREATE TABLE IF NOT EXISTS buyers (
    buyer_phone TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Token Transactions Table: Maps individual meters to buyers
CREATE TABLE IF NOT EXISTS token_transactions (
    meter_number TEXT PRIMARY KEY,
    buyer_phone TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 0.0 CHECK (balance >= 0.0),
    daily_usage REAL NOT NULL DEFAULT 3.0 CHECK (daily_usage > 0.0),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_phone) REFERENCES buyers(buyer_phone) ON DELETE CASCADE
);

-- 3. Alert History Table: Logs sent SMS warnings
CREATE TABLE IF NOT EXISTS alert_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meter_number TEXT NOT NULL,
    buyer_phone TEXT NOT NULL,
    balance_at_alert REAL NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meter_number) REFERENCES token_transactions(meter_number)
);