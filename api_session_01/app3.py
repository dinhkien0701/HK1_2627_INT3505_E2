from flask import Flask, jsonify, request
from uuid import uuid4
# Code bài 3
app = Flask(__name__)

# ĐÂY LÀ CÁCH DUY NHẤT để chỉnh jsonify() trả về tiếng Việt
app.json.ensure_ascii = False  

STUDENTS = []
@app.route("/students", methods = ["POST"])
def create_student():
    body = request.get_json(silent=True) or {}
    name = body.get("name")
    if not name:
        return jsonify({"error":"name là bắt buộc"}), 400
    student = {
        "id": str(uuid4()),
        "name": name,
        "gpa": body.get("gpa", 0.0)
    }
    STUDENTS.append(student)
    return {"id": student.get("id"), "name": student.get("name"), "gpa":student.get("gpa")}, 201

# Code lấy từ hai bài đầu
# GET /health - kiểm tra server còn sống
@app.route("/health", methods = ["GET"])
def health():
    return jsonify({"status" : "ok"}), 200
# POST /echo - trả lại cái client cho người gửi
@app.route("/echo", methods = ["POST"])
def echo():
    data = request.get_json(silent = True) or {}
    return jsonify({"you_sent": data}), 200
@app.route("/")
def index():
    return {"message": "Hello, API!"}
if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 5000, debug = True)
