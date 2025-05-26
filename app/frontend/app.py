from flask import Flask, render_template, request, redirect # type: ignore
import requests
import os

app = Flask(__name__)

# Backend API service URL (Kubernetes will resolve this via DNS)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5000")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        if content:
            requests.post(f"{BACKEND_URL}/notes", json={"content": content})
        return redirect("/")

    # GET: fetch notes
    response = requests.get(f"{BACKEND_URL}/notes")
    notes = response.json() if response.ok else []
    return render_template("index.html", notes=notes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
