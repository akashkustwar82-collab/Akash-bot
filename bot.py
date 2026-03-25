from fbchat import Client
from fbchat.models import *
import json, time

class MessengerBot(Client):

    def __init__(self, cookies, log_func=None):
        self.log = log_func

        # 🔥 FINAL FIX (important)
        super().__init__(email="", password="", session_cookies=cookies)

    def onReady(self):
        if self.log:
            self.log("✅ Bot Connected")

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):

        if not message or not message.text:
            return

        with open("config.json") as f:
            config = json.load(f)

        admin = str(config["admin_uid"])

        if str(author_id) != admin:
            return

        msg = message.text.lower()

        # 🔥 COMMANDS
        if msg == "lock on":
            config["lock_name"] = True
            self.send(Message(text="🔒 Name Lock ON"), thread_id, thread_type)

        elif msg == "lock off":
            config["lock_name"] = False
            self.send(Message(text="🔓 Name Lock OFF"), thread_id, thread_type)

        elif msg.startswith("setname"):
            name = message.text.replace("setname ", "")
            config["group_name"] = name
            self.send(Message(text=f"✅ Name set: {name}"), thread_id, thread_type)

        elif msg == "nick on":
            config["lock_nick"] = True
            self.send(Message(text="🔒 Nick Lock ON"), thread_id, thread_type)

        elif msg == "nick off":
            config["lock_nick"] = False
            self.send(Message(text="🔓 Nick Lock OFF"), thread_id, thread_type)

        elif msg == "status":
            status = f"Name Lock: {config['lock_name']}\nNick Lock: {config['lock_nick']}"
            self.send(Message(text=status), thread_id, thread_type)

        with open("config.json","w") as f:
            json.dump(config,f,indent=4)

    def monitor(self):
        while True:
            try:
                with open("config.json") as f:
                    config = json.load(f)

                group_id = config["group_id"]

                if not group_id:
                    time.sleep(5)
                    continue

                info = self.fetchThreadInfo(group_id)[group_id]

                # 🔒 NAME LOCK
                if config["lock_name"]:
                    if info.name != config["group_name"]:
                        self.changeThreadTitle(config["group_name"], group_id)
                        if self.log:
                            self.log("🔒 Name Locked")

                # 🔒 NICK LOCK
                if config["lock_nick"]:
                    members = info.participants
                    nicknames = config.get("nicknames", {})

                    if not nicknames:
                        for u in members:
                            nicknames[u] = info.nicknames.get(u, "")

                        config["nicknames"] = nicknames
                        with open("config.json","w") as f:
                            json.dump(config,f,indent=4)

                        if self.log:
                            self.log("💾 Nicknames Saved")

                    for u in members:
                        current = info.nicknames.get(u,"")
                        saved = nicknames.get(u,"")

                        if current != saved:
                            self.changeNickname(saved, u, group_id)
                            if self.log:
                                self.log(f"🔒 Nick Locked: {u}")

                time.sleep(5)

            except Exception as e:
                if self.log:
                    self.log(f"❌ Error: {e}")
                time.sleep(5)
