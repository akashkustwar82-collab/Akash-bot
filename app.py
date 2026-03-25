import requests
import json
import time

class MessengerBot:

    def __init__(self, cookies, log_func=None):
        self.session = requests.Session()
        self.log = log_func

        for c in cookies:
            self.session.cookies.set(c["key"], c["value"])

    def log_msg(self, msg):
        if self.log:
            self.log(msg)

    def check_login(self):
        try:
            r = self.session.get("https://mbasic.facebook.com/")
            if "logout" in r.text.lower():
                self.log_msg("✅ Cookies Login Success")
                return True
            else:
                self.log_msg("❌ Invalid Cookies")
                return False
        except:
            self.log_msg("❌ Network Error")
            return False

    def monitor(self):
        while True:
            try:
                with open("config.json") as f:
                    config = json.load(f)

                self.log_msg("👀 Monitoring running...")

                # ⚠️ NOTE:
                # Facebook official API नहीं है यहाँ
                # इसलिए group control limited रहेगा

                time.sleep(10)

            except Exception as e:
                self.log_msg(f"❌ Error: {e}")
                time.sleep(5)
                
