import os
import pickle
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

SECRET_KEY = "hardcoded_secret_123"

@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.form.get("data")
    obj = pickle.loads(bytes.fromhex(data))
    return jsonify({"message": "Deserialization complete", "data": str(obj)})

@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
