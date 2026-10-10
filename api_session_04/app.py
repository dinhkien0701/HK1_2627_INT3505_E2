"""Tasks API — Flask app: /openapi.json + /docs + 5 endpoints."""

import uuid
from datetime import datetime, timezone

import yaml
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load spec
with open("openapi.yaml", encoding="utf-8") as f:
    OPENAPI_SPEC = yaml.safe_load(f)

# Swagger UI
SWAGGER_HTML = """
<!DOCTYPE html><html><head><title>Tasks API</title>
<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui.css">
</head><body><div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui-bundle.js"></script>
<script src="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui-standalone-preset.js"></script>
<script>
window.onload = () => SwaggerUIBundle({
  url: "/openapi.json", dom_id: "#swagger-ui",
  tryItOutEnabled: true, presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset]
});
</script></body></html>
"""

# In-memory data
TASKS = {
    "3fa85f64-5717-4562-b3fc-2c963f66afa6": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "title": "Họp nhóm API team",
        "status": "open",
        "priority": "high",
        "dueDate": "2026-09-15",
        "assigneeId": "9c8a7f64-5717-4562-b3fc-2c963f66afa6",
    }
}

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def err(status, title, detail):
    return jsonify({"title": title, "status": status,
                    "detail": detail, "instance": request.path}), status

# Routes phục vụ spec + docs
@app.get("/openapi.json")
def spec_json():
    return jsonify(OPENAPI_SPEC)

@app.get("/docs")
def docs():
    return render_template_string(SWAGGER_HTML)

@app.get("/")
def index():
    return '<meta http-equiv="refresh" content="0; url=/docs">'

# 5 endpoints
@app.get("/v1/tasks")
def list_tasks():
    try:
        limit = int(request.args.get("limit", 20))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return err(400, "Bad Request", "limit/offset phải là số nguyên")
    if not 1 <= limit <= 100:
        return err(400, "Bad Request", "limit phải trong 1-100")
    if offset < 0:
        return err(400, "Bad Request", "offset phải >= 0")

    items = list(TASKS.values())
    s = request.args.get("status")
    if s:
        if s not in ("open", "done"):
            return err(400, "Bad Request", "status phải là open/done")
        items = [t for t in items if t["status"] == s]

    return jsonify({"items": items[offset:offset + limit],
                    "total": len(items), "limit": limit, "offset": offset})

@app.post("/v1/tasks")
def create_task():
    d = request.get_json(silent=True) or {}
    title = d.get("title")
    if not isinstance(title, str) or not 1 <= len(title) <= 200:
        return err(422, "Validation Error", "title bắt buộc, 1-200 ký tự")
    priority = d.get("priority", "normal")
    if priority not in ("low", "normal", "high"):
        return err(422, "Validation Error", "priority phải là low/normal/high")

    tid = str(uuid.uuid4())
    task = {"id": tid, "title": title, "status": "open", "priority": priority,
            "dueDate": d.get("dueDate"), "assigneeId": d.get("assigneeId")}
    TASKS[tid] = task

    res = jsonify(task)
    res.status_code = 201
    res.headers["Location"] = f"/v1/tasks/{tid}"
    return res

@app.get("/v1/tasks/<task_id>")
def get_task(task_id):
    t = TASKS.get(task_id)
    return jsonify(t) if t else err(404, "Not Found", f"Không có task {task_id}")

@app.patch("/v1/tasks/<task_id>")
def patch_task(task_id):
    t = TASKS.get(task_id)
    if not t:
        return err(404, "Not Found", f"Không có task {task_id}")
    d = request.get_json(silent=True) or {}
    if not d:
        return err(422, "Validation Error", "Body phải có ít nhất 1 field")

    for k in ("title", "status", "priority", "dueDate", "assigneeId"):
        if k in d:
            t[k] = d[k]
    return jsonify(t)

@app.delete("/v1/tasks/<task_id>")
def delete_task(task_id):
    if task_id not in TASKS:
        return err(404, "Not Found", f"Không có task {task_id}")
    del TASKS[task_id]
    return "", 204

if __name__ == "__main__":
    print("Swagger UI: http://localhost:5000/docs")
    app.run(host="0.0.0.0", port=5000, debug=True)