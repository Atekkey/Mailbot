import json
import os


def get_id_to_alias():
    with open("names.json", "r+") as f:
        id_to_alias = json.load(f)
        return id_to_alias

def get_alias_to_id():
    with open("names.json", "r+") as f:
        id_to_alias = json.load(f)
        alias_to_id = {val: key for key, val in id_to_alias.items()}
        return alias_to_id

def add_alias(id, alias):
    with open("names.json", "r+") as f:
        id_to_alias = json.load(f)

    if(id not in id_to_alias):
        id_to_alias[id] = [alias]
    else: # Id exists
        id_to_alias[id].append(alias)
        id_to_alias[id] = list(set(id_to_alias[id])) # avoid dups

    with open("names.json", "w") as f:
        json.dump(id_to_alias, f, indent=2)

def remove_id(id):
    with open("names.json", "r+") as f:
        id_to_alias = json.load(f)
    aliases = []
    if(id in id_to_alias):
        aliases = id_to_alias[id]
        del id_to_alias[id]
    
    with open("names.json", "w") as f:
        json.dump(id_to_alias, f, indent=2)
    return aliases