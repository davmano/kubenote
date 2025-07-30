from flask import Flask, render_template, request, redirect # type: ignore
import requests
import os

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST # type: ignore

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

# Backend API service URL (Kubernetes will resolve this via DNS)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5000")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        REQUEST_COUNT.labels(method="POST", endpoint="/").inc()
        content = request.form.get("content")
        if content:
            requests.post(f"{BACKEND_URL}/notes", json={"content": content})
        return redirect("/")

    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    # GET: fetch notes
    response = requests.get(f"{BACKEND_URL}/notes")
    notes = response.json() if response.ok else []
    return render_template("index.html", notes=notes)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
