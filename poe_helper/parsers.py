"""Parse text from PoE into a dictionary.

Functions:
    item_parser
"""

import re

# list of possible properties
WEAPON_PROPERTIES = [
    "Physical Damage:", 
    "Elemental Damage:", 
    "Critical Strike Chance:", 
    "Attacks per Second:", 
    "Weapon Range:", 
    "One Handed", 
    "Two Handed", 
    "Wand", 
    "Staff", 
    "Dagger", 
    "Claw",
    "Bow"
]

ARMOUR_PROPERTIES = [
    "Chance to Block:", 
    "Armour:", 
    "Energy Shield:", 
    "Evasion Rating:"
]


def item_parser(text):
    """Parses item text copied from PoE Trade or the game.

    Args:
        text (str): Raw copied text.
    
    Returns:
        A dictionary with parsed key, value pairs.
    
    """

    text_list = [i.lstrip("\n").splitlines() for i in text.split("--------")]
    # create dictionary with key, value "requirements", list of requirements
    text_dict = {
        text_list[idx].pop(idx_2).strip(":") : _dict_of_req(text_list, idx)  
        for idx, sublist in enumerate(text_list[:]) 
        for idx_2, item in enumerate(sublist[:]) 
        if item in ["Requirements:"]
    }

    if ['Unidentified'] in text_list:
        text_dict["identified"] = False
        text_dict["type"] = text_list[0].pop()
        text_list.remove(['Unidentified'])
    else:
        text_dict["type"] = text_list[0].pop()
        text_dict["name"] = text_list[0].pop()

    if ['Corrupted'] in text_list:
        text_dict["corrupted"] = True
        text_list.remove(['Corrupted'])

    _item_parser_iterator(text_list, text_dict)
    text_list = list(filter(None, text_list)) 
    # remove all empty lists after parsing
    
    if text_list:     # extract explicit mods if list is not empty
        text_dict["explicitMods"] = text_list[0]
        del text_list[0]

    # at this point list should be empty unless it is a unique
    # in which case it will have flavor text as well which we can delete

    del text_list
    return text_dict


def _dict_of_req(text_list, idx):   
    # for use in dict comprehension turns the requirements into dicts as well
    req_list = text_list[idx][1:]
    req_dict = {}
    for req in req_list:
        x = req.split(':')
        req_dict[x[0]] = x[1].strip()
    del text_list[idx][1:]
    return req_dict


def _item_parser_iterator(text_list, text_dict):
    for i in text_list[:]: # use copy of list to avoid iterating over a mutating list
        if isinstance(i, list):
            _item_parser_iterator(i, text_dict=text_dict)
        else:
            _item_parser_classify(i, text_list, text_dict=text_dict)


def _item_parser_classify(i, text_list, text_dict): 
    implicit_re = re.compile(r'.*(\(implicit\))$')
    # identify and classify parts of the list
    if implicit_re.match(i) is not None:    # regex match to find implicit mods
        if "implicit" not in text_dict:
            text_dict["implicitMods"] = [i]
        else:
            text_dict["implicitMods"].append(i)
        text_list.remove(i)
    elif any(prop in i for prop in ARMOUR_PROPERTIES and WEAPON_PROPERTIES):  # check to see if properties
        split = i.split(":")
        if len(split) == 2:
            if "properties" not in text_dict:   # create dict entry if it doesn't exist
                text_dict["properties"] = {split[0]:split[1].strip()}
            else:
                text_dict["properties"][split[0]] = split[1].strip()
        text_list.remove(i)
    else:   # any remaining info.. ex sockets, item level, notes
        split = i.split(":")
        if len(split) == 2:
            text_dict[split[0]] = split[1].strip()
            text_list.remove(i)