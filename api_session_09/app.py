from flask import Flask, jsonify, request

from gateway import dispatch

app = Flask(__name__)


@app.route("/orders", methods=["POST"])
def create_order():
    which, result = dispatch(request.get_json())
    response = jsonify(result)
    response.headers["X-Order-Handler"] = which
    return response, 201 if which == "v2" else 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)