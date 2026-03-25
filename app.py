from flask import Flask, render_template, request, jsonify
import threading, json, time
from bot import MessengerBot

app = Flask(__name__)

logs = []
bot_running = False
session_status = "Not Connected"

def log(msg):
    print(msg)
    logs.append(msg)
    if len(logs) > 100:
        logs.pop(0)

def run_bot():
    global bot_running, session_status

    while bot_running:
        try:
            with open("config.json") as f:
                config = json.load(f)

            bot = MessengerBot(config["cookies"], log)

            if not bot.check_login():
                session_status = "❌ Invalid Cookies"
                time.sleep(5)
                continue

            session_status = "✅ Logged In"
            log("🚀 Bot Started")

            bot.monitor()

        except Exception as e:
            log(f"❌ Crash: {e}")
            time.sleep(5)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        try:
            data = {
                "cookies": json.loads(request.form["cookies"]),
                "admin_uid": request.form["admin_uid"],
                "group_id": request.form["group_id"],
                "group_name": request.form["group_name"]
            }

            with open("config.json","w") as f:
                json.dump(data,f,indent=4)

            log("💾 Config Saved")

        except:
            log("❌ Invalid Input")

    return render_template("index.html",status=bot_running,session=session_status)

@app.route("/start")
def start():
    global bot_running
    if not bot_running:
        bot_running = True
        threading.Thread(target=run_bot).start()
        log("▶️ Bot Started")
    return "started"

@app.route("/stop")
def stop():
    global bot_running
    bot_running = False
    log("⏹ Bot Stopped")
    return "stopped"

@app.route("/logs")
def get_logs():
    return jsonify(logs)

app.run(host="0.0.0.0",port=5000)
