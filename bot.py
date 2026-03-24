from fbchat import Client
from fbchat.models import *
import json

class MessengerBot(Client):

    def __init__(self, *args, stats=None, log_func=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats = stats
        self.log = log_func

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):

        if self.stats:
            self.stats["messages"] += 1

        with open("config.json") as f:
            config = json.load(f)

        admin_id = config["admin_uid"]

        if str(author_id) != str(admin_id):
            return

        msg = message.text.lower()

        if msg == "ping":
            self.send(Message(text="pong"), thread_id, thread_type)

        elif msg == "nickname":
            self.changeNickname("🔥 BOT", author_id, thread_id)

        elif msg == "groupname":
            self.changeThreadTitle("🔥 My Group", thread_id)

        if self.stats:
            self.stats["commands"] += 1
