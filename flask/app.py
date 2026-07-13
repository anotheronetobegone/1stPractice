from flask import Flask, jsonify
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


if __name__ == "__main__":
    app.run(debug=True)