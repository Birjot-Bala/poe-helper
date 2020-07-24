# poe_helper.py

from gui import Gui

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
# item_rarity = example_list[0]
# item_name = example_list[1]
# item_type = example_list[2]

gui = Gui()

gui.master.title('POE Helper')
gui.master.resizable(False,False)

gui.mainloop()