from flask import Flask, request, jsonify # type: ignore
import psycopg2 # type: ignore
import os

# Prometheus imports
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST # type: ignore

app = Flask(__name__)

# 🔹 Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

# Load database config from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "notesdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/notes", methods=["GET"])
def get_notes():
    REQUEST_COUNT.labels(method="GET", endpoint="/notes").inc()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM notes ORDER BY id DESC;")
    notes = [{"id": row[0], "content": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(notes)

@app.route("/notes", methods=["POST"])
def add_note():
    REQUEST_COUNT.labels(method="POST", endpoint="/notes").inc()
    data = request.get_json()
    content = data.get("content", "")
    if not content:
        return jsonify({"error": "Content is required"}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (content) VALUES (%s) RETURNING id;", (content,))
    note_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": note_id, "content": content}), 201

@app.route("/")
def health_check():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    return "KubeNote Backend is running!", 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# This code is the backend service for KubeNote, a simple note-taking application.
