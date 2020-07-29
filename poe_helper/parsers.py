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

def format_clipboard(text):
    split_text = text.split('--------')
    split_text_name =split_text[0].split('\n')
    item_rarity = split_text_name[0]
    item_name = split_text_name[1]
    item_type = split_text_name[2]
    return item_rarity, item_name, item_type

def item_parser(text):

    text_list = [i.lstrip("\n").splitlines() for i in text.split("--------")]

    text_dict = {text_list[idx][idx_2].strip(":") : text_list[idx][1:]  # create dictionary with key requirements and values all requirements
        for idx, sublist in enumerate(text_list) 
        for idx_2, item in enumerate(sublist) 
        if item in ["Requirements:"]
    }

    if ['Unidentified'] in text_list:
        text_dict["identified"] = False
    
    if ['Corrupted'] in text_list:
        text_dict["corrupted"] = True
    
    implicit_re = re.compile(r'.*(\(implicit\))$')
    text_dict["implicit"] = []
    for i in chain.from_iterable(text_list):
        if implicit_re.match(i) is not None: # regex match to find implicit mods
            text_dict["implicit"].append(i)
        split = i.split(":")
        if len(split) > 1:
            text_dict[split[0]] = split[1].strip()
        # elif colon_re.match(i) is not None:
        #     split = i.split(":")
        #     text_dict[split[0]] = split[1].strip()

    pprint.pprint(text_list)
    print(text_dict)

item_parser(example_text)
item_parser(example2)

