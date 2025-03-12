# Slack.py
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

BOTTOKEN = os.environ.get("BOTTOKEN")
APPTOKEN = os.environ.get("APPTOKEN")

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialize the Slack app
app = App(token=BOTTOKEN)

# Listen for direct messages
@app.event("message")
def handle_dm(event, say):
    user_id = event["user"]
    text = event["text"]

    # Only respond if it's a DM
    if event.get("channel_type") == "im":
        print(f"Received DM from {user_id}: {text}")
        say(f"Hey <@{user_id}>, I got your message: '{text}'")

# Start the bot using Socket Mode
if __name__ == "__main__":
    handler = SocketModeHandler(app, APPTOKEN)
    handler.start()


