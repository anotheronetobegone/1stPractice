import sqlite3
from typing import Optional, List
import pandas as pd

conn = sqlite3.connect('practice.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS students (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     course TEXT NOT NULL,
#     score REAL DEFAULT 0.0
# )
# ''')
# conn.commit()
# print('Table Created Successfully')

DB_PATH = "practice.db"
 
def run_query(query: str, params: tuple = ()) -> list[dict]:
    """Run a SELECT query and return results as a list of dicts."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]
 
def run_query_no_output(query: str, params: tuple = ()) -> None:
    """Run an INSERT, UPDATE, DELETE or CREATE query. No return value."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, params)
        conn.commit()

def insert_student(conn, name: str, course: str, score: float) -> None:
    """Insert a new student record into the database."""
    conn.execute(
        "INSERT INTO students (name, course, score) VALUES (?, ?, ?)",
        (name, course, score)
    )
    conn.commit()


def update_score(conn, student_id: int, new_score: float) -> None:
    """Update the score for a given student."""
    conn.execute(
        "UPDATE students SET score = ? WHERE id = ?",
        (new_score, student_id)
    )
    conn.commit()

def create_students_table() -> None:
    run_query_no_output('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            score REAL DEFAULT 0.0
        )
    ''')

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

def print_all_students() -> None:
    rows = run_query("SELECT * FROM students")
    for row in rows:
        print(row)

def run_query_one(query: str, params: tuple = ()) -> Optional[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None

def pandas_filter_above_70(csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    filtered = df[df["score"] > 70].sort_values("score", ascending=False)
    print(filtered[["name", "score"]].to_string(index=False))

def sqlite_filter_above_70() -> None:
    rows = run_query(
        "SELECT name, score FROM students WHERE score > ? ORDER BY score DESC",
        (70,)
    )
    for row in rows:
        print(row)

# print(run_query('select * from students'))

# create_students_table()
# insert_sample_students()
# print_all_students())

# student = run_query_one("SELECT * FROM students WHERE name = ?", ("Bob",))
# print(student)

# pandas_filter_above_70('practice.csv')