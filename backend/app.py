from flask import Flask, jsonify
from flask_cors import CORS
import os

from db.models import User


app = Flask(__name__)
frontend_url = os.getenv("FRONTEND_URL", "*")
CORS(app, origins=[frontend_url])

@app.route("/")
def hello():
    row = User.select().first()
    return jsonify({"message": f"First entry: {row.name}" if row else "No data found"})


@app.route("/user/<int:user_id>")
def get_user(user_id):
    try:
        user = User.get(User.id == user_id)
        return jsonify({
            "id": user.id,
            "name": user.name,
            "avatar": user.avatar,
            "preferences": user.preferences
        })
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))