import mysql.connector
from mysql.connector import MySQLConnection
from typing import Optional, List, Dict

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "P@55w0rD",
    "database": "practice",
}

def mysql_connect(use_db: bool = True) -> MySQLConnection:
    config = MYSQL_CONFIG.copy()
    if not use_db:
        config.pop("database", None)
    return mysql.connector.connect(**config)

def run_query(query: str, params: tuple = ()) -> List[Dict]:
    with mysql_connect() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchall()

def run_query_no_output(query: str, params: tuple = ()) -> None:
    with mysql_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

def run_query_one(query: str, params: tuple = ()) -> Optional[Dict]:
    with mysql_connect() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchone()

def create_database() -> None:
    with mysql_connect(use_db=False) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS practice")
        conn.commit()

def create_students_table() -> None:
    run_query_no_output('''
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            course VARCHAR(255) NOT NULL,
            score DOUBLE DEFAULT 0.0
        )
    ''')

def insert_sample_students() -> None:
    run_query_no_output(
        "INSERT INTO students (name, course, score) VALUES (%s, %s, %s)",
        ("Alice", "Math", 88.5),
    )
    run_query_no_output(
        "INSERT INTO students (name, course, score) VALUES (%s, %s, %s)",
        ("Bob", "Science", 72.0),
    )
    run_query_no_output(
        "INSERT INTO students (name, course, score) VALUES (%s, %s, %s)",
        ("Cara", "History", 95.0),
    )

def print_all_students() -> None:
    rows = run_query("SELECT * FROM students")
    for row in rows:
        print(row)

def find_student_by_name(name: str) -> Optional[Dict]:
    return run_query_one(
        "SELECT * FROM students WHERE name = %s",
        (name,),
    )

def mysql_filter_above_70() -> None:
    rows = run_query(
        "SELECT name, score FROM students WHERE score > %s ORDER BY score DESC",
        (70,),
    )
    for row in rows:
        print(row)

create_database()
create_students_table()
insert_sample_students()

print("All students:")
print_all_students()

print("\nFind Bob:")
print(find_student_by_name("Bob"))

print("\nStudents scoring above 70:")
mysql_filter_above_70()