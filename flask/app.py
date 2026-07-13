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
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    name = (data.get("name") or "").strip()
    course = (data.get("course") or "").strip()
    score = data.get("score", 0.0)

    if not name or not course:
        return jsonify({"error": "name and course are required"}), 400

    try:
        score = float(score)
    except (TypeError, ValueError):
        return jsonify({"error": "score must be a number"}), 400

    db.run_query_no_output(
        "INSERT INTO students (name, course, score) VALUES (?, ?, ?)",
        (name, course, score),
    )

    new_student = db.run_query_one(
        "SELECT * FROM students ORDER BY id DESC LIMIT 1"
    )
    return jsonify(new_student), 201

if __name__ == "__main__":
    app.run(debug=True)