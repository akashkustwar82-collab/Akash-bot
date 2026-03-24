from flask import Flask, render_template, request
import json

app = Flask(__name__)

def save_config(data):
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    with open("config.json") as f:
        return json.load(f)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = load_config()

        data["cookies"] = request.form["cookies"]
        data["group_id"] = request.form["group_id"]
        data["admin_id"] = request.form["admin_id"]

        save_config(data)
        return "✅ Saved! Bot restart karo"

    return render_template("index.html")

app.run(host="0.0.0.0", port=10000)
