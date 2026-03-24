from fbchat import Client
from fbchat.models import *

class MessengerBot(Client):
    def onReady(self):
        print("✅ Bot Started Successfully!")

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        if author_id != self.uid:
            msg = message.text.lower()

            if msg == "nickname":
                self.changeNickname("🔥 KING", author_id, thread_id)
                self.send(Message(text="Nickname Changed"), thread_id, thread_type)

            elif msg == "groupname":
                self.changeThreadTitle("🔥 My Locked Group", thread_id)
                self.send(Message(text="Group Name Changed"), thread_id, thread_type)

            elif msg == "lockname":
                self.changeThreadTitle("🔒 Locked Name", thread_id)
