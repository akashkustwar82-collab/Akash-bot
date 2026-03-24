from flask import Flask, render_template, request, jsonify
import threading
import json
from bot import MessengerBot

app = Flask(__name__)

bot_thread = None
bot_running = False
logs = []   # 🔥 Logs store करने के लिए

def add_log(msg):
    logs.append(msg)
    if len(logs) > 50:
        logs.pop(0)

def run_bot():
    global bot_running
    try:
        add_log("🚀 Bot Starting...")

        with open("config.json") as f:
            config = json.load(f)

        bot = MessengerBot(session_cookies=config["cookies"])

        add_log("✅ Bot Logged In")

        bot.listen()

    except Exception as e:
        add_log(f"❌ Error: {str(e)}")
    finally:
        bot_running = False
        add_log("🛑 Bot Stopped")

@app.route("/", methods=["GET", "POST"])
def index():
    global bot_thread, bot_running

    if request.method == "POST":
        action = request.form.get("action")

        if action == "start" and not bot_running:
            bot_thread = threading.Thread(target=run_bot)
            bot_thread.start()
            bot_running = True
            add_log("▶️ Start Button Clicked")

        elif action == "stop":
            bot_running = False
            add_log("⏹ Stop Button Clicked")

    return render_template("index.html", status=bot_running)

# 🔥 Logs API
@app.route("/logs")
def get_logs():
    return jsonify(logs)

app.run(host="0.0.0.0", port=5000)
