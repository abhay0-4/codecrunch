import sqlite3
import json
from problems import PROBLEMS

DB = "codecrunch.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT UNIQUE NOT NULL,
            email      TEXT UNIQUE NOT NULL,
            password   TEXT NOT NULL,
            is_admin   INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            desc       TEXT NOT NULL,
            test_cases TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            problem_id   INTEGER NOT NULL,
            code         TEXT NOT NULL,
            language     TEXT NOT NULL DEFAULT 'python',
            verdict      TEXT NOT NULL,
            submitted_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()

    # Add language column if upgrading from older DB
    try:
        conn.execute("ALTER TABLE submissions ADD COLUMN language TEXT DEFAULT 'python'")
        conn.commit()
    except Exception:
        pass  # column already exists

    # Seed problems from problems.py if table is empty
    count = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
    if count == 0:
        for pid, prob in PROBLEMS.items():
            conn.execute(
                "INSERT INTO problems (title, difficulty, desc, test_cases) VALUES (?, ?, ?, ?)",
                (prob["title"], prob["difficulty"], prob["desc"],
                 json.dumps(prob["test_cases"]))
            )
        conn.commit()

    conn.close()


def get_problems():
    conn = get_db()
    rows = conn.execute("SELECT * FROM problems ORDER BY id").fetchall()
    conn.close()
    return [
        {
            "id":         row["id"],
            "title":      row["title"],
            "difficulty": row["difficulty"],
            "desc":       row["desc"],
            "test_cases": json.loads(row["test_cases"])
        }
        for row in rows
    ]


def get_problem(pid):
    conn = get_db()
    row = conn.execute("SELECT * FROM problems WHERE id = ?", (pid,)).fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id":         row["id"],
        "title":      row["title"],
        "difficulty": row["difficulty"],
        "desc":       row["desc"],
        "test_cases": json.loads(row["test_cases"])
    }