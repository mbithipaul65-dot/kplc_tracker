import sqlite3

def simulate_token_drain(meter_number="37192840192", drain_amount=0.5):
    """Simulates power consumption by deducting units, creating the record if missing."""
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    
    # Ensure table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meter_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meter_number TEXT NOT NULL,
            current_units REAL NOT NULL,
            daily_consumption REAL NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if meter exists
    cursor.execute('SELECT current_units, daily_consumption FROM meter_readings WHERE meter_number = ? ORDER BY updated_at DESC LIMIT 1', (meter_number,))
    row = cursor.fetchone()
    
    if row:
        # Update existing record
        new_units = max(0.0, row[0] - drain_amount)
        cursor.execute('''
            UPDATE meter_readings 
            SET current_units = ? 
            WHERE meter_number = ?
        ''', (new_units, meter_number))
        daily_rate = row[1]
    else:
        # Seed initial record if missing (e.g., 6.5 units, 3.5 daily rate)
        new_units = 6.5
        daily_rate = 3.5
        cursor.execute('''
            INSERT INTO meter_readings (meter_number, current_units, daily_consumption)
            VALUES (?, ?, ?)
        ''', (meter_number, new_units, daily_rate))
        print(f"[SIMULATION] Seeded initial row for meter {meter_number}.")

    conn.commit()
    conn.close()
    
    print(f"[SIMULATION] Meter {meter_number} updated.")
    print(f" -> Current Units Left: {new_units:.1f} units")
    print(f" -> Daily Consumption: {daily_rate:.1f} units/day")
    print(f" -> Dynamic Threshold (2 Days): {daily_rate * 2:.1f} units")

if __name__ == "__main__":
    simulate_token_drain()