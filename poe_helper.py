# poe_helper.py
import tkinter as tk

from constants import TRADE_BASE_URL
from services import search_trade_api, format_search_query, ApiRequests

# create api object using trade url
poe_trade_api = ApiRequests(TRADE_BASE_URL)

# # TODO: format text for search query 
# example_text = r"""Rarity: Unique
# The Pariah
# Unset Ring
# --------
# Requirements:
# Level: 60
# --------
# Sockets: R 
# --------
# Item Level: 84
# --------
# Has 1 Socket (implicit)
# --------
# +2 to Level of Socketed Gems
# 6% increased Attack and Cast Speed
# +100 to Maximum Life per Red Socket
# +100 to Maximum Mana per Green Socket
# +100 to Maximum Energy Shield per Blue Socket
# 15% increased Item Quantity per White Socket
# --------
# A man who changes his loyalties often,
# soon finds he has none.
# --------
# Corrupted
# """
# example_list = example_text.split('--------')
# print(example_list)
# example_list = example_list[0].split('\n')
# print(example_list)
# item_name = example_list[1]
# item_type = example_list[2]

# search for item
search_pariah = format_search_query("The Pariah", "Unset Ring")
response_pariah = search_trade_api(search_pariah, poe_trade_api)

# print results
print('\n\n'.join([item.item_info() for item in response_pariah]))
