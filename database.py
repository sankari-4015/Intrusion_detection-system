import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    duration INTEGER,
                    src_bytes INTEGER,
                    dst_bytes INTEGER,
                    count INTEGER,
                    risk TEXT
                )''')
    conn.commit()
    conn.close()

def insert_log(duration, src_bytes, dst_bytes, count, risk):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, duration, src_bytes, dst_bytes, count, risk) VALUES (?, ?, ?, ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               duration, src_bytes, dst_bytes, count, risk))
    conn.commit()
    conn.close()

def get_counts():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT risk, COUNT(*) FROM logs GROUP BY risk")
    data = dict(c.fetchall())
    conn.close()
    return data