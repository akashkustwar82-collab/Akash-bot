from flask import Flask, render_template, request, jsonify
import threading, json, time
from bot import MessengerBot

app = Flask(__name__)

bot_thread = None
bot_running = False
logs = []
session_status = "Not Checked"

# 📊 Stats
stats = {
    "messages": 0,
    "commands": 0,
    "start_time": None
}

def add_log(msg):
    logs.append(msg)
    if len(logs) > 100:
        logs.pop(0)

def run_bot():
    global bot_running, session_status

    try:
        add_log("🚀 Bot Starting...")

        with open("config.json") as f:
            config = json.load(f)

        bot = MessengerBot(
            session_cookies=config["cookies"],
            stats=stats,
            log_func=add_log
        )

        session_status = "✅ Valid Session"
        stats["start_time"] = time.time()

        add_log("✅ Login Success")
        bot.listen()

    except Exception as e:
        session_status = "❌ Invalid Session"
        add_log(f"❌ Error: {str(e)}")

    finally:
        bot_running = False
        add_log("🛑 Bot Stopped")

@app.route("/", methods=["GET", "POST"])
def index():
    global bot_running, bot_thread

    if request.method == "POST":

        action = request.form.get("action")

        if action == "save":
            try:
                data = {
                    "cookies": json.loads(request.form.get("cookies")),
                    "admin_uid": request.form.get("admin_uid"),
                    "bot_uid": request.form.get("bot_uid")
                }

                with open("config.json", "w") as f:
                    json.dump(data, f, indent=4)

                add_log("💾 Config Saved")

            except:
                add_log("❌ Invalid Cookies JSON")

        elif action == "start" and not bot_running:
            bot_thread = threading.Thread(target=run_bot)
            bot_thread.start()
            bot_running = True
            add_log("▶️ Bot Started")

        elif action == "stop":
            bot_running = False
            add_log("⏹ Bot Stopped")

    return render_template("index.html",
                           status=bot_running,
                           session=session_status)

@app.route("/logs")
def get_logs():
    return jsonify(logs)

@app.route("/stats")
def get_stats():
    uptime = 0
    if stats["start_time"]:
        uptime = int(time.time() - stats["start_time"])

    return jsonify({
        "messages": stats["messages"],
        "commands": stats["commands"],
        "uptime": uptime
    })

app.run(host="0.0.0.0", port=5000)
