from flask import Flask, jsonify, request
import db

app = Flask(__name__)
db.init_db()


@app.route("/hello")
def hello():
    return "Hello, World!"


@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(db.run_query("SELECT * FROM students"))


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = db.run_query_one(
        "SELECT * FROM students WHERE id = ?",
        (student_id,),
    )
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student)

@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "data not provided"}), 400
    
    name = (data.get("name") or "").strip()
    course = (data.get("course") or "").strip()

    if not name or not course:
        return jsonify({"error": "name and course are required"}), 400

    score = data.get("score", 0.0)
    
    db.run_query_no_output('INSERT INTO students (name, course, score) VALUES (?, ?, ?)',
                           (data["name"], data["course"], data.get("score", 0.0)))
    return jsonify(db.run_query_one('SELECT * FROM students ORDER BY id DESC LIMIT 1')), 201

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = db.run_query_one(
        "SELECT * FROM students WHERE id = ?",
        (student_id,),
    )
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    
    data = request.get_json()
    db.run_query_no_output('UPDATE students SET name = ?, course = ?, score = ? WHERE id = ?', (data["name"], data["course"], data.get("score", 0.0), student_id))
    return jsonify(db.run_query_one('SELECT * FROM students WHERE id = ?', (student_id,))), 200

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = db.run_query_one(
        "SELECT * FROM students WHERE id = ?",
        (student_id,),
    )
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    
    db.run_query_no_output("DELETE FROM students WHERE id = ?", (student_id,))
    return jsonify({"message" : f'Student {student_id} deleted'})

if __name__ == "__main__":
    app.run(debug=True)