# Slack.py
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from Handle_Names import get_id_to_alias, get_alias_to_id


def notify_user(alias):
    BOTTOKEN = os.environ.get("BOTTOKEN")
    app = App(token=BOTTOKEN)

    alias_to_id = get_alias_to_id()
    id = alias_to_id[alias]
    
    resp = app.client.conversations_open(users=[id])

    outNameList = alias.lower().split(" ")
    outName = " ".join([n.capitalize() for n in outNameList])
    app.client.chat_postMessage(channel=resp["channel"]["id"], text=f"{outName}, You have Mail!")

def notify_sender(alias, startId):
    BOTTOKEN = os.environ.get("BOTTOKEN")
    app = App(token=BOTTOKEN)
    id = startId
    try:
        outNameList = alias.lower().split(" ")
        outName = " ".join([n.capitalize() for n in outNameList])
        resp = app.client.conversations_open(users=[id])
        app.client.chat_postMessage(channel=resp["channel"]["id"], text=f"{outName}'s Mail Proccesed.")
    except Exception as e:
        print(f"Error notifying sender: {e}")
        return False

def set_bot_status(status = "away"):
    
    BOTTOKEN = os.environ.get("BOTTOKEN")
    app = App(token=BOTTOKEN)

    try:
        app.client.users_setPresence(presence=status)
        return True
    except Exception as e:
        print(e)
        return False

    

    


