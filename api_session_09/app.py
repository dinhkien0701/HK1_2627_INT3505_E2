from flask import Flask
from datetime import datetime, timezone

from sunset import deprecate_at

app = Flask(__name__)
V1_SUNSET = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)


@app.route("/api/v1/users/<int:uid>")
@deprecate_at(V1_SUNSET, replacement="/api/v2/users")
def get_v1_user(uid):
    return {"id": uid, "full_name": "Nguyễn Văn A"}


if __name__ == "__main__":
    app.run(port=5000, debug=True)