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
        except Exception as e:
            self.log_msg(f"❌ Network Error: {e}")
            return False

    def monitor(self):
        while True:
            try:
                self.log_msg("👀 Bot Running...")

                # ⚠️ Note:
                # Facebook private API access नहीं है
                # इसलिए direct group rename / nickname change नहीं होगा

                time.sleep(10)

            except Exception as e:
                self.log_msg(f"❌ Error: {e}")
                time.sleep(5)
