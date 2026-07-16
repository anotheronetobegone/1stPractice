import os
import sqlite3
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.db")


def run_query(query: str, params: tuple = ()) -> list[dict]:
    """Run a SELECT query and return results as a list of dicts."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def run_query_no_output(query: str, params: tuple = ()) -> None:
    """Run an INSERT, UPDATE, DELETE or CREATE query."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, params)
        conn.commit()


def run_query_one(query: str, params: tuple = ()) -> Optional[dict]:
    """Run a SELECT query and return one row or None."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None


def create_students_table() -> None:
    run_query_no_output(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            score REAL DEFAULT 0.0
        )
        """
    )


def insert_sample_students() -> None:
    run_query_no_output(
        "INSERT INTO students (name, course, score) VALUES (?, ?, ?)",
        ("Alice", "Math", 88.5),
    )
    run_query_no_output(
        "INSERT INTO students (name, course, score) VALUES (?, ?, ?)",
        ("Bob", "Science", 72.0),
    )
    run_query_no_output(
        "INSERT INTO students (name, course, score) VALUES (?, ?, ?)",
        ("Cara", "History", 95.0),
    )


def init_db() -> None:
    create_students_table()