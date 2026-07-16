from flask import Flask, jsonify, request
import db
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

db.init_db()

@app.route("/api/dashboard", methods=["GET", "OPTIONS"])
def get_dashboard():
    if request.method == "OPTIONS":
        return "", 204
 
    return jsonify({
        "overview": {
            "average_assessment_score": "78.54",
            "average_feedback_score": "4.13",
            "total_attendees": 507,
            "total_completions": 468,
            "total_planned_participants": 543,
            "total_sessions": 20,
            "total_training_cost": "605000.00"
        },
        "monthly_trend": [],
        "category_breakdown": [],
        "recent_sessions": [],
        "status": "ok"
    })

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