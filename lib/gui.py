# gui.py

import tkinter as tk
from tkinter import ttk

from lib.services import format_search_query, search_trade_api, poe_trade_api, format_clipboard

class Gui(ttk.Frame):

    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent, padding=10)
        self.grid(column=0, row=0)
        self.createWidgets()


    def createWidgets(self):
        self.search_button = ttk.Button(self, text="Search", command=self.output_results)
        self.price_label_frame = ttk.LabelFrame(self, text="")

        self.search_button.grid(column=0, row=1, pady=10)
        self.price_label_frame.grid(column=0, row=0, padx=10)

    
    def output_results(self):
        for child in self.price_label_frame.winfo_children():
            child.destroy()
        self.price_label_frame.config(text="")
        clipboard = self.clipboard_get()
        try:
            item_name, item_type = format_clipboard(clipboard)
            self.price_label_frame.config(text=f'{item_name}\n{item_type}')
            item_dict = format_search_query(item_name, item_type)
            trade_response = search_trade_api(item_dict, poe_trade_api)
            for counter, item in enumerate(trade_response):
                self.price_title_label = ttk.Label(self.price_label_frame, text=f'{counter+1}:')
                self.price_result_label = ttk.Label(self.price_label_frame, text=item.format_price())

                self.price_result_label.grid(column=1, row=counter, sticky="e", padx=10, pady=2)
                self.price_title_label.grid(column=0, row=counter, padx=10)
        except:
            self.except_label = ttk.Label(self.price_label_frame, text="Incorrect format of text in clipboard.")

            self.except_label.grid(column=0, row=0)


