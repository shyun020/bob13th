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

@app.route("/sql_injection", methods=["GET"])
def sql_injection():
    user_input = request.args.get("user_input")
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return jsonify({"data": result})

@app.route("/os_command_injection", methods=["GET"])
def os_command_injection():
    user_input = request.args.get("command")
    os.system(user_input)
    return jsonify({"message": "Command executed"})

@app.route("/insecure_cookie", methods=["GET"])
def insecure_cookie():
    user_id = request.cookies.get("user_id")
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return jsonify({"data": result})

@app.route("/hardcoded_credentials", methods=["POST"])
def hardcoded_credentials():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "admin" and password == "admin123":
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
