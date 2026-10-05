from flask import Flask, jsonify, request
import uuid
app = Flask(__name__)

# database

posts_db = {}
comments_db = {}

# tao va lay bai viet

@app.route("/api/v1/posts", methods = ['GET', 'POST'])
def handle_posts():
    # Tra danh sach bai viet
    if request.method == 'GET':
        return jsonify(list(posts_db.values())), 200

    # Dang 1 bai viet
    if request.method == 'POST':
        data = request.json
        post_id = str(uuid.uuid4()) # dung uuid
        new_post = {
            "id" : post_id,
            "title" : data.get("title"),
            "content" : data.get("content")

        }
        posts_db[post_id] = new_post
        return jsonify(new_post), 201

# doc bai viet

@app.route("/api/v1/posts/<post_id>",methods = ['GET'])
def get_post(post_id):
    post = posts_db.get(post_id)
    if not post:
        return jsonify({"error": "Khong tim thay bai dang theo yeu cau "}), 404
    return jsonify(post), 200

# Dang comment vaf xem danh sach comment cua bai viet (post) nao do theo post_id

@app.route("/api/v1/posts/<post_id>/comments", methods = ['GET', 'POST'])
def handle_comment(post_id):
    if post_id not in posts_db:
        return jsonify({"error": "Khong tim thay bai dang theo yeu cau "}), 404

    if request.method == 'GET':
        post_comments = [ c for c in comments_db.values() if c["post_id"] == post_id]
        return jsonify(post_comments), 200

    if request.method == 'POST':
        data = request.json
        comment_id = str(uuid.uuid4())
        new_comment = {
            "id" : comment_id,
            "post_id" : post_id,
            "text" : data.get("text")

        }
        comments_db[comment_id] = new_comment
        return jsonify(new_comment), 201

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 5000 , debug = True)


