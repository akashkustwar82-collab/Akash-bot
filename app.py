from flask import Flask, render_template, request, jsonify
import threading, json, time
from bot import MessengerBot

app = Flask(__name__)

logs = []
bot_running = False

def log(msg):
    print(msg)
    logs.append(msg)
    if len(logs) > 100:
        logs.pop(0)

def run_bot():
    global bot_running

    while bot_running:
        try:
            with open("config.json") as f:
                config = json.load(f)

            bot = MessengerBot(config["cookies"], log)

            log("🚀 Bot Started")

            threading.Thread(target=bot.monitor, daemon=True).start()

            bot.listen()

        except Exception as e:
            log(f"❌ Crash: {e}")
            log("🔁 Reconnecting...")
            time.sleep(5)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        try:
            data = {
                "cookies": json.loads(request.form["cookies"]),
                "admin_uid": request.form["admin_uid"],
                "group_id": request.form["group_id"],
                "group_name": request.form["group_name"],
                "lock_name": True,
                "lock_nick": True,
                "nicknames": {}
            }

            with open("config.json","w") as f:
                json.dump(data,f,indent=4)

            log("💾 Config Saved")

        except:
            log("❌ Invalid Input")

    return render_template("index.html", status=bot_running)

@app.route("/start")
def start():
    global bot_running
    if not bot_running:
        bot_running = True
        threading.Thread(target=run_bot).start()
        log("▶️ Started")
    return "ok"

@app.route("/stop")
def stop():
    global bot_running
    bot_running = False
    log("⏹ Stopped")
    return "ok"

@app.route("/logs")
def get_logs():
    return jsonify(logs)

app.run(host="0.0.0.0", port=5000)
