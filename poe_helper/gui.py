# gui.py

import tkinter as tk
from tkinter import ttk

from services import (
    format_search_query, search_trade_api, poe_trade_api,
    image_from_url
)
from parsers import item_parser

class Gui(ttk.Frame):
    """Base class for the graphical user interface (GUI).

    """

    def __init__(self, parent=None):
        """The constructor for the Gui class."""
        ttk.Frame.__init__(self, parent, padding=10)
        self.grid(column=0, row=0)
        self.grid_columnconfigure(0, weight=1)
        self.createWidgets()


    def createWidgets(self):
        """Initial widge creation."""
        self.search_button = ttk.Button(self, text="Search", command=self.output_results)
        self.price_label_frame = ttk.LabelFrame(self, text="")
        self.search_button.grid(column=0, row=1, pady=10, sticky="s")
        self.price_label_frame.grid(column=0, row=0, padx=10)

    
    def output_results(self):
        """Retrieves and processes copied text from the clipboard.

        Function creates labels of the listings retrieved and shows 
        an image of the item. If the copied text is not compatible
        displays an error message.

        """
        for child in self.price_label_frame.winfo_children(): 
            # destroy all widgets in price label frame
            child.destroy()

        self.price_label_frame.config(text="")
        clipboard = self.clipboard_get()

        try:
            parsed_item = item_parser(clipboard) 
            item_dict = format_search_query(parsed_item["name"], parsed_item["type"])
            trade_response = search_trade_api(item_dict, poe_trade_api)

            for counter, item in enumerate(trade_response):
                self.price_title_label = ttk.Label(self.price_label_frame, text=f'{counter+1}:')
                self.price_result_label = ttk.Label(self.price_label_frame, text=item.format_price())
                self.price_result_label.grid(column=1, row=counter+10, sticky="e", padx=10, pady=2)
                self.price_title_label.grid(column=0, row=counter+10, padx=10)

            self.price_label_frame.config(text=f'{parsed_item["name"]}\n{parsed_item["type"]}')
            image_url = trade_response[0].item_icon()
            photo = image_from_url(image_url)
            self.listing_label = ttk.Label(self.price_label_frame, text="Listings:")
            self.listing_label.grid(column=0, row=1)
            self.item_image_label = ttk.Label(self.price_label_frame, image=photo)
            self.item_image_label.image = photo
            self.item_image_label.grid(column=0, row=0, columnspan=2, pady=5)
    
        except:
            self.except_label = ttk.Label(self.price_label_frame, text="Incorrect format of text in clipboard.")
            self.except_label.grid(column=0, row=0)


