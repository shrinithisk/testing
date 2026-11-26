import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)")
    c.execute("INSERT INTO users (username, role) VALUES ('admin', 'superuser')")
    c.execute("INSERT INTO users (username, role) VALUES ('alice', 'developer')")
    conn.commit()
    return conn

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Sphere Testing Application"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/user')
def get_user():
    username = request.args.get('username', '')
    conn = get_db()
    cursor = conn.cursor()
    # SQL Injection flaw (Semgrep detection target)
    query = f"SELECT id, username, role FROM users WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"id": user[0], "username": user[1], "role": user[2]})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
