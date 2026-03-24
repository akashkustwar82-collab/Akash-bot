import json
import time
from fbchat import Client
from fbchat.models import ThreadType

def load_config():
    with open("config.json") as f:
        return json.load(f)

def save_config(data):
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

class Bot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        config = load_config()

        if author_id == config["admin_id"]:
            msg = message_object.text.lower()

            # SET NAME
            if msg.startswith("!setname"):
                name = message_object.text.replace("!setname ", "")
                config["group_name"] = name
                save_config(config)
                self.changeThreadTitle(name, thread_id=thread_id, thread_type=thread_type)
                self.send(Message(text=f"✅ Group name set: {name}"), thread_id, thread_type)

            # LOCK NAME
            if msg == "!lockname on":
                config["lock_name"] = True
                save_config(config)
                self.send(Message(text="🔒 Name Lock ON"), thread_id, thread_type)

            if msg == "!lockname off":
                config["lock_name"] = False
                save_config(config)
                self.send(Message(text="🔓 Name Lock OFF"), thread_id, thread_type)

            # SET NICKNAME
            if msg.startswith("!setnick"):
                nick = message_object.text.replace("!setnick ", "")
                config["nickname"] = nick
                save_config(config)

                users = self.fetchThreadInfo(thread_id)[thread_id].participants
                for user in users:
                    self.changeNickname(nick, user, thread_id=thread_id, thread_type=thread_type)

                self.send(Message(text=f"👑 Nickname set: {nick}"), thread_id, thread_type)

            # LOCK NICK
            if msg == "!locknick on":
                config["lock_nick"] = True
                save_config(config)
                self.send(Message(text="🔒 Nick Lock ON"), thread_id, thread_type)

            if msg == "!locknick off":
                config["lock_nick"] = False
                save_config(config)
                self.send(Message(text="🔓 Nick Lock OFF"), thread_id, thread_type)

            # STATUS
            if msg == "!status":
                status = f"""
📊 BOT STATUS

Name Lock: {config['lock_name']}
Nick Lock: {config['lock_nick']}
Group Name: {config['group_name']}
Nickname: {config['nickname']}
"""
                self.send(Message(text=status), thread_id, thread_type)

def run_bot():
    config = load_config()
    bot = Bot(session_cookies=config["cookies"])

    while True:
        try:
            config = load_config()
            info = bot.fetchThreadInfo(config["group_id"])
            group = info[config["group_id"]]

            # NAME LOCK
            if config["lock_name"] and group.name != config["group_name"]:
                bot.changeThreadTitle(config["group_name"],
                                      thread_id=config["group_id"],
                                      thread_type=ThreadType.GROUP)

            # NICK LOCK
            if config["lock_nick"]:
                for user in group.participants:
                    bot.changeNickname(config["nickname"], user,
                                       thread_id=config["group_id"],
                                       thread_type=ThreadType.GROUP)

            time.sleep(15)

        except Exception as e:
            print("Error:", e)
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
