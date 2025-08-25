# Slack.py
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import signal

BOTTOKEN = os.environ.get("BOTTOKEN")
APPTOKEN = os.environ.get("APPTOKEN")

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from Handle_Names import add_alias, remove_id, get_id_to_alias


app = App(token=BOTTOKEN)
signal.signal(signal.SIGPIPE, signal.SIG_IGN) # Ignore SIGPIPE

def safe_say(message, say):
    try:
        say(message)
    except Exception as e:
        void = 1

@app.event("message")
def handle_dm(event, say):
    USAGE = "Usage: [Start|List|Remove User] OR [Add] [First] [Last]"

    user_id = event["user"]
    text = event["text"].upper().strip()
    textSplit = text.strip().split(" ")
    if event.get("channel_type") != "im":
        return
    
    if(textSplit[0] == "ADD" and len(textSplit) >= 3):
        name = " ".join(textSplit[1:])
        safe_say(f"Adding name: {name}...", say)
        add_alias(user_id, name)
        safe_say("Done!", say)
        return
    
    if((textSplit[0] == "REMOVE" and textSplit[1] == "USER") and len(textSplit) == 2):
        safe_say(f"Removing self...", say)
        aliases = remove_id(user_id)
        if(aliases == []):
            safe_say("No aliases found.", say)
            return
        safe_say(f"Removed Aliases: {aliases}", say)
        return
    
    if(len(textSplit) == 1):
        if(textSplit[0] == "START" or textSplit[0] == "INIT"):
            safe_say(f"Started!", say)
            os.environ["STARTUSER"] = user_id
            print("UID: ", user_id)
            os._exit(0)

        if(textSplit[0] == "ADMINKILL" and user_id == "U06DP4P5DC6"):
            safe_say(f"KILLED", say)
            os._exit(-4)
        
        if(textSplit[0] == "LIST"):
            id_to_alias = get_id_to_alias()
            aliases = id_to_alias.get(user_id)
            safe_say(f"Aliases: {aliases}", say)
            return
        
        if(textSplit[0] == "HELP"):
            safe_say(USAGE, say)
            return
    
    safe_say("Unknown Statement.\n" + USAGE, say)



# Start the bot using Socket Mode
handler = SocketModeHandler(app, APPTOKEN)
handler.start()


