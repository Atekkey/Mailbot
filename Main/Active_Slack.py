import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from Handle_Names import get_id_to_alias, get_alias_to_id


def notify_user(alias): # Tells User they have mail
    BOTTOKEN = os.environ.get("BOTTOKEN")
    app = App(token=BOTTOKEN)

    alias_to_id = get_alias_to_id() # Fetch User Id from Alias
    id = alias_to_id[alias]
    
    resp = app.client.conversations_open(users=[id])

    outNameList = alias.lower().split(" ")
    outName = " ".join([n.capitalize() for n in outNameList])
    app.client.chat_postMessage(channel=resp["channel"]["id"], text=f"{outName}, You have Mail!") # DM the user

def notify_sender(alias, startId): # Tells scanning user they have scanned the mail
    BOTTOKEN = os.environ.get("BOTTOKEN")
    app = App(token=BOTTOKEN)
    id = startId # Init User Id
    try:
        outNameList = alias.lower().split(" ")
        outName = " ".join([n.capitalize() for n in outNameList]) # Get Name
        resp = app.client.conversations_open(users=[id])
        app.client.chat_postMessage(channel=resp["channel"]["id"], text=f"{outName}'s Mail Proccesed.")
    except Exception as e:
        print(f"Error notifying sender: {e}")
        return False

def notify_sender_ended(startId): # Tell Init User scanner is closed
    BOTTOKEN = os.environ.get("BOTTOKEN")
    app = App(token=BOTTOKEN)
    id = startId
    try:
        resp = app.client.conversations_open(users=[id])
        app.client.chat_postMessage(channel=resp["channel"]["id"], text=f"Scanner Closed.")
    except Exception as e:
        print(f"Error notifying sender: {e}")
        return False

def set_bot_status(status = "away"): # Unused function. Slack no longer allows bot status to be set.
    BOTTOKEN = os.environ.get("BOTTOKEN")
    app = App(token=BOTTOKEN)

    try:
        app.client.users_setPresence(presence=status)
        return True
    except Exception as e:
        print(e)
        return False

    

    


