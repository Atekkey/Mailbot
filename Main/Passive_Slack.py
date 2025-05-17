# Slack.py
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

BOTTOKEN = os.environ.get("BOTTOKEN")
APPTOKEN = os.environ.get("APPTOKEN")

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from Handle_Names import add_alias, remove_id

app = App(token=BOTTOKEN)
print("Passive, PID: ", str(os.getpid()))

@app.event("message")
def handle_dm(event, say):
    user_id = event["user"]
    text = event["text"].upper().strip()
    textSplit = text.strip().split(" ")
    if event.get("channel_type") != "im":
        return
    
    if(textSplit[0] == "ADD"):
        name = " ".join(textSplit[1:])
        say(f"Adding name: {name}...")
        add_alias(user_id, name)
        say("Done!")
        return
    
    if(textSplit[0] == "REMOVE" and textSplit[1] == "USER"):
        say(f"Removing self...")
        aliases = remove_id(user_id)
        if(aliases == []):
            say("No aliases found.")
            return
        say(f"Removed Aliases: {aliases}")
        return
    
    if(textSplit[0] == "START" or textSplit[0] == "INIT"):
        say(f"Initializing...")
        say(f"Started!")
        os._exit(0)

    if(textSplit[0] == "ADMINKILL"):
        say(f"KILLED")
        os._exit(-4)
    
    say("Unknown Statement.\nUsage: [Start|Remove User] OR [Add] [First] [Last]")


# Start the bot using Socket Mode
handler = SocketModeHandler(app, APPTOKEN)
handler.start()


