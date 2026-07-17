from flask import Flask, jsonify, request
import sqlite3
import db

app = Flask(__name__)
 
@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response
 
@app.route("/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
 
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
 
    conn.close()
 
    return jsonify(students)
 
@app.route("/api/dashboard", methods=["GET", "OPTIONS"])
def get_dashboard():
    if request.method == "OPTIONS":
        return "", 204

    overview = db.get_overview()

    return jsonify({
        "overview": overview,
        "status": "ok"
    })
 
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
 
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
 
    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (data["name"], data["age"], data["course"])
    )
 
    conn.commit()
    conn.close()
 
    return {"message": "Student added successfully"}, 201
 
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
 
    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()
 
    conn.close()
 
    if student:
        return jsonify(student)
    else:
        return jsonify({"message": "Student not found"}), 404
   
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "data not provided"}), 400

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?",
        (data.get("name"), data.get("age"), data.get("course"), student_id)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": f"Student {student_id} updated successfully"}), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": f"Student {student_id} deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)