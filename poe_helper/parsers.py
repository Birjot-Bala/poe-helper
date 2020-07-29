import pprint
import re
from itertools import chain
from timeit import timeit

example_text = r"""Rarity: Unique
The Pariah
Unset Ring
--------
Requirements:
Level: 60
--------
Sockets: R 
--------
Item Level: 84
--------
Has 1 Socket (implicit)
--------
+2 to Level of Socketed Gems
6% increased Attack and Cast Speed
+100 to Maximum Life per Red Socket
+100 to Maximum Mana per Green Socket
+100 to Maximum Energy Shield per Blue Socket
15% increased Item Quantity per White Socket
--------
A man who changes his loyalties often,
soon finds he has none.
--------
Corrupted"""

example2 = r"""Rarity: Unique
Superior Astral Plate
--------
Quality: +7% (augmented)
Armour: 761 (augmented)
--------
Requirements:
Strength: 180
--------
Sockets: R-R 
--------
Item Level: 75
--------
+9% to all Elemental Resistances (implicit)
--------
Unidentified
--------
Note: ~price 1 chaos
"""

example3 = r"""Rarity: Unique
Unset Ring
--------
Sockets: G 
--------
Item Level: 84
--------
Has 1 Socket (implicit)
--------
Unidentified
--------
Note: ~b/o 20 chaos
"""

example4 = r"""Rarity: Rare
Rift Mantle
Sacrificial Garb
--------
Armour: 645 (augmented)
Evasion Rating: 680 (augmented)
Energy Shield: 147 (augmented)
--------
Requirements:
Level: 72
Str: 66
Dex: 66
Int: 66
--------
Sockets: R-W-G 
--------
Item Level: 72
--------
+18 to Evasion Rating
96% increased Armour, Evasion and Energy Shield
+11 to maximum Energy Shield
+62 to maximum Mana
+41% to Cold Resistance
+34% to Lightning Resistance
21% increased Stun and Block Recovery
--------
Corrupted
--------
Note: ~price 1 chaos
"""

def format_clipboard(text):
    split_text = text.split('--------')
    split_text_name =split_text[0].split('\n')
    item_rarity = split_text_name[0]
    item_name = split_text_name[1]
    item_type = split_text_name[2]
    return item_rarity, item_name, item_type

def item_parser(text):

    text_list = [i.lstrip("\n").splitlines() for i in text.split("--------")]

    def dict_of_req(idx):   # for use in dict comprehension: turns the requirements into dicts as well
        req_list = text_list[idx][1:]
        req_dict ={}
        for req in req_list:
            x = req.split(':')
            req_dict[x[0]] = x[1].strip()
        del text_list[idx][1:]
        return req_dict

    text_dict = {text_list[idx].pop(idx_2).strip(":") : dict_of_req(idx)  # create dictionary with key, value "requirements", list of requirements
        for idx, sublist in enumerate(text_list) 
        for idx_2, item in enumerate(sublist) 
        if item in ["Requirements:"]
    }

    text_list = list(filter(None, text_list))


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
    
    implicit_re = re.compile(r'.*(\(implicit\))$')

    for i in text_list:
        if implicit_re.match(i) is not None: # regex match to find implicit mods
            if "implicit" not in text_dict:
                text_dict["implicit"] = [i]
            else:
                text_dict["implicit"].append(i)
            text_list.remove([i])
        
        else:
            split = i.split(":")
            if len(split) > 1:
                text_dict[split[0]] = split[1].strip()
                text_list.remove([i])
        # elif colon_re.match(i) is not None:
        #     split = i.split(":")
        #     text_dict[split[0]] = split[1].strip()

    pprint.pprint(text_list)
    print(text_dict)

# item_parser(example_text)
# print('='*60)
# item_parser(example2)
# print('='*60)
# item_parser(example3)
# print('='*60)
item_parser(example4)
