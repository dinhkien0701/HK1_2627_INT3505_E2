from functools import wraps

from flask import Flask
from flask import jsonify, request

LATEST = "2"
SUPPORTED = ("1", "2", "2024-06-20")
USERS = {
    1: {"f": "Văn", "l": "Nguyễn", "e": "a@vnu.vn"},
}


def api_version(supported=SUPPORTED, default=LATEST):
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            version = request.headers.get("X-API-Version", default)
            if version not in supported:
                return jsonify(error="unsupported version"), 400

            result = fn(version, *args, **kwargs)
            response = jsonify(result)
            response.headers["X-API-Version-Served"] = version
            return response

        return wrapper

    return decorate


app = Flask(__name__)


@app.route("/users/<int:uid>")
@api_version()
def get_user(version, uid):
    user = USERS.get(uid)
    if user is None:
        return {"error": "not found"}

    if version == "1":
        return {"id": uid, "full_name": f"{user['f']} {user['l']}"}

    return {
        "id": uid,
        "first_name": user["f"],
        "last_name": user["l"],
        "email": user["e"],
    }


if __name__ == "__main__":
    app.run(port=5000, debug=True)