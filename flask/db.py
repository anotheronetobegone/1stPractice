import os
import sqlite3
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.db")


def _connect():
    return sqlite3.connect(DB_PATH)


def run_query(query: str, params: tuple = ()) -> list[dict]:
    conn = _connect()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def run_query_no_output(query: str, params: tuple = ()) -> None:
    conn = _connect()
    conn.execute(query, params)
    conn.commit()
    conn.close()


def run_query_one(query: str, params: tuple = ()) -> Optional[dict]:
    conn = _connect()
    conn.row_factory = sqlite3.Row
    row = conn.execute(query, params).fetchone()
    conn.close()
    return dict(row) if row else None


def create_students_table() -> None:
    run_query_no_output(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT NOT NULL
        )
        """
    )


def get_overview() -> dict:
    students = run_query("SELECT * FROM students")

    total_students = len(students)
    average_age = 0

    if total_students:
        average_age = round(
            sum(student.get("age", 0) or 0 for student in students) / total_students,
            2
        )

    course_breakdown = {}
    for student in students:
        course = student.get("course", "Unknown")
        course_breakdown[course] = course_breakdown.get(course, 0) + 1

    return {
        "total_students": total_students,
        "average_age": average_age,
        "course_breakdown": course_breakdown,
        "latest_students": students[-5:] if students else []
    }


def init_db() -> None:
    create_students_table()