import os
import pickle
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

SECRET_KEY = "hardcoded_secret_123"

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    c.execute(query)
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user": user})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/ping", methods=["GET"])
def ping():
    ip = request.args.get("ip")
    response = os.system(f"ping -c 3 {ip}")
    return jsonify({"status": "Ping executed", "result": response})

@app.route("/greet", methods=["GET"])
def greet():
    message = request.args.get("message")
    return f"<h1>{message}</h1>"

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
