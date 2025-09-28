import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import signal

from functions import setUID # Get my Functions from other files
from Handle_Names import add_alias, remove_id, get_id_to_alias

BOTTOKEN = os.environ.get("BOTTOKEN") # Necessary Env tokens
APPTOKEN = os.environ.get("APPTOKEN")

app = App(token=BOTTOKEN) # Init Slack Listener
signal.signal(signal.SIGPIPE, signal.SIG_IGN) # Ignore SIGPIPE

def safe_say(message, say): # Method to safely say something, ignoring errors
    try:
        say(message)
    except Exception as e:
        void = 1

@app.event("message")
def handle_dm(event, say):
    USAGE = "Usage: [Start|List|Remove User] OR [Add] [First] [Last]" # User Help Message

    user_id = event["user"]
    text = event["text"].upper().strip()
    textSplit = text.strip().split(" ")
    if event.get("channel_type") != "im": # Only respond to DMs
        return
    
    if(textSplit[0] == "ADD" and len(textSplit) >= 3): # User adds Alias
        name = " ".join(textSplit[1:])
        safe_say(f"Adding name: {name}...", say)
        add_alias(user_id, name)
        safe_say("Done!", say)
        return
    
    if((textSplit[0] == "REMOVE" and textSplit[1] == "USER") and len(textSplit) == 2): # User Removes Self
        safe_say(f"Removing self...", say)
        aliases = remove_id(user_id)
        if(aliases == []):
            safe_say("No aliases found.", say)
            return
        safe_say(f"Removed Aliases: {aliases}", say)
        return
    
    if(len(textSplit) == 1):
        if(textSplit[0] == "START" or textSplit[0] == "INIT"): # User starts up text scanner
            safe_say(f"Started!", say)
            setUID(user_id) # Stores User Id in a text file
            os.kill(os.getppid(), signal.SIGUSR1) # Send a "move on" signal to the parent process
            return
            # os._exit(0)

        if(textSplit[0] == "ADMINKILL" and user_id == "U06DP4P5DC6"): # Admin kills scanner
            safe_say(f"KILLED", say)
            os.kill(os.getppid(), signal.SIGUSR2) # Sends a kill signal to parent process
            return
        
        if(textSplit[0] == "LIST"): # Lists user aliases
            id_to_alias = get_id_to_alias()
            aliases = id_to_alias.get(user_id)
            safe_say(f"Aliases: {aliases}", say)
            return
        
        if(textSplit[0] == "HELP"): # Shows the help message
            safe_say(USAGE, say)
            return
    
    safe_say("Unknown Statement.\n" + USAGE, say) # If nothing else matches, show help message


# Start the bot using Socket Mode
handler = SocketModeHandler(app, APPTOKEN)
handler.start()


