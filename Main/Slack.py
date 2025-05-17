# Slack.py
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

BOTTOKEN = os.environ.get("BOTTOKEN")
APPTOKEN = os.environ.get("APPTOKEN")

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=BOTTOKEN)

@app.event("message")
def handle_dm(event, say):
    user_id = event["user"]
    text = event["text"].upper().strip()
    textSplit = text.strip().split(" ")
    if event.get("channel_type") != "im":
        return
    
    # if(textSplit[0] == "ADD"):
    #     say(f"Adding name: { " ".join(textSplit[1:]) }")
    
    if(textSplit[0] == "START"):
        say(f"Initializing...")

        say(f"Started!")



# Start the bot using Socket Mode
if __name__ == "__main__":
    handler = SocketModeHandler(app, APPTOKEN)
    handler.start()


