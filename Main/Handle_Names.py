import json
import os
import regex as re

def get_id_to_alias(): # Make Id to Alias Dict
    with open("names.json", "r+") as f:
        id_to_alias = json.load(f)
        return id_to_alias

def get_alias_to_id(): # Make Alias to Id Dict
    with open("names.json", "r+") as f:
        alias_to_id = {}
        id_to_alias = json.load(f)
        for id in id_to_alias:
            for alias in id_to_alias[id]:
                alias_to_id[alias] = id
        return alias_to_id

def add_alias(id, alias): # Add Alias for User
    with open("names.json", "r+") as f:
        id_to_alias = json.load(f)

    if(id not in id_to_alias):
        id_to_alias[id] = [alias]
    else: # Id exists
        id_to_alias[id].append(alias)
        id_to_alias[id] = list(set(id_to_alias[id])) # avoid dups

    with open("names.json", "w") as f:
        json.dump(id_to_alias, f, indent=2)

def remove_id(id): # Remove User and return their aliases
    with open("names.json", "r+") as f:
        id_to_alias = json.load(f)
    aliases = []
    if(id in id_to_alias):
        aliases = id_to_alias[id]
        del id_to_alias[id]
    
    with open("names.json", "w") as f:
        json.dump(id_to_alias, f, indent=2)
    return aliases

def generate_list(): # Get all Aliases
    alias_list = []
    with open("names.json", "r+") as f:
        id_to_alias = json.load(f)
        for key in id_to_alias:
            for alias in id_to_alias[key]:
                alias_list.append(alias)
    alias_list = list(set(alias_list)) # avoid dups
    return alias_list

def strCompareToList(names, longStr): # Looks for all aliases in a long string, returns first found
    for name in names:
        if(re.search(name, longStr) != None):
            return name
    return ""