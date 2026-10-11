import sqlite3

def setup_database():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    # Apply table structures from schema.sql
    with open("schema.sql", "r") as sql_file:
        cursor.executescript(sql_file.read())

    # Seed test buyers and meter mappings
    cursor.execute("SELECT COUNT(*) FROM buyers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO buyers (buyer_phone) VALUES (?)",
            [("+254740395206",), ("+254712345678",)]
        )
        cursor.executemany(
            "INSERT INTO token_transactions (meter_number, buyer_phone, balance, daily_usage) VALUES (?, ?, ?, ?)",
            [
                ("01402938475", "+254740395206", 14.0, 3.5),
                ("01928374650", "+254740395206", 3.2, 4.0),
                ("01234567890", "+254712345678", 7.5, 2.5)
            ]
        )

    conn.commit()
    conn.close()
    print("[SUCCESS] Schema updated and database initialized.")

if __name__ == "__main__":
    setup_database()