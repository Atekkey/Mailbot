# Slack.py
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from Handle_Names import get_id_to_alias, get_alias_to_id


def notify_user(alias):
    BOTTOKEN = os.environ.get("BOTTOKEN")
    APPTOKEN = os.environ.get("APPTOKEN")
    app = App(token=BOTTOKEN)
    # handler = SocketModeHandler(app, APPTOKEN)

    alias_to_id = get_alias_to_id()
    id = alias_to_id[alias]
    
    resp = app.client.conversations_open(users=[id])
    app.client.chat_postMessage(channel=resp["channel"]["id"], text=f"{alias}, You have Mail!")

def set_bot_status(text, emoji):
    BOTTOKEN = os.environ.get("BOTTOKEN")
    app = App(token=BOTTOKEN)

    profile = {
        "status_text": text,
        "status_emoji": emoji,
        "status_expiration": 0 
    }
    try:
        app.client.users_profile_set(profile=profile)
        return True
    except Exception as e:
        return False

    

    


