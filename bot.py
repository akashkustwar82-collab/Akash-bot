from fbchat import Client
import json, time

class MessengerBot(Client):

    def __init__(self, cookies, log_func=None):
        self.cookies = cookies
        self.log = log_func

        # 🔥 IMPORTANT FIX
        super().__init__(email=None, password=None, session_cookies=cookies)

    def onReady(self):
        if self.log:
            self.log("✅ Bot Connected")

    def monitor_group(self):
        while True:
            try:
                with open("config.json") as f:
                    config = json.load(f)

                group_id = config["group_id"]
                desired_name = config["group_name"]
                nicknames = config.get("nicknames", {})

                if not group_id:
                    time.sleep(5)
                    continue

                info = self.fetchThreadInfo(group_id)[group_id]

                # 🔒 Group name lock
                if info.name != desired_name:
                    self.changeThreadTitle(desired_name, group_id)
                    self.log("🔒 Group Name Locked")

                members = info.participants

                # 🔒 Save nicknames first time
                if not nicknames:
                    for u in members:
                        nicknames[u] = info.nicknames.get(u, "")

                    config["nicknames"] = nicknames
                    with open("config.json", "w") as f:
                        json.dump(config, f, indent=4)

                    self.log("💾 Nicknames Saved")

                # 🔒 Lock nicknames
                for u in members:
                    current = info.nicknames.get(u, "")
                    saved = nicknames.get(u, "")

                    if current != saved:
                        self.changeNickname(saved, u, group_id)
                        self.log(f"🔒 Nickname Locked: {u}")

                time.sleep(5)

            except Exception as e:
                self.log(f"❌ Monitor Error: {e}")
                time.sleep(5)
