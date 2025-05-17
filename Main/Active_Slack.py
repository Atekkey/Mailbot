# Slack.py
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
# from Handle_Names import get_id_to_alias, get_alias_to_id


def notify_user(id):
    BOTTOKEN = os.environ.get("BOTTOKEN")
    APPTOKEN = os.environ.get("APPTOKEN")
    app = App(token=BOTTOKEN)
    handler = SocketModeHandler(app, APPTOKEN)
    
    resp = app.client.conversations_open(users=[id])
    app.client.chat_postMessage(channel=resp["channel"]["id"], text="You have a package!")

    

    


