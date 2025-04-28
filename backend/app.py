from flask import Flask, jsonify
from flask_cors import CORS
import os
from db import db, Test, initialize_db

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080", "http://127.0.0.1:8080"])


# Always initialize DB on startup
with app.app_context():
    initialize_db()

@app.route("/")
def hello():
    row = Test.select().first()
    return jsonify({"message": f"First entry: {row.name}" if row else "No data found"})

@app.route("/user/<int:user_id>")
def get_user(user_id):
    # Dummy data for now, replace with your DB query if needed
    return jsonify({"id": user_id, "name": f"User {user_id}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))