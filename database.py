import sqlite3

DB_NAME = "missing_persons.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS persons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        location TEXT,
        image_data TEXT,
        status TEXT DEFAULT 'Missing'
    )
    """)

    conn.commit()
    conn.close()


def insert_person(name,email,location,image_data):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT INTO persons(name,email,location,image_data,status) VALUES(?,?,?,?,?)",
        (name,email,location,image_data,"Missing")
    )

    conn.commit()
    conn.close()


def get_all_persons():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM persons")
    rows = c.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def mark_found(pid):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("UPDATE persons SET status='Found' WHERE id=?", (pid,))

    conn.commit()
    conn.close()


def escalate_alert(pid):
    print("Alert triggered")