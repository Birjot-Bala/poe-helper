# poe_helper.py
import argparse

from poe_helper.gui import Gui
from poe_helper.bot import bot
from poe_helper.settings import DISCORD_TOKEN


def build_gui():
    gui = Gui()

    gui.master.title('POE Helper')
    gui.master.resizable(False,False)
    gui.master.minsize(200,100)
    gui.master.grid_columnconfigure(0, weight=1)

    gui.mainloop()


def run_bot():
    bot.run(DISCORD_TOKEN)


def cmd_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bot", help="Connects the Discord Bot", 
                        action="store_true")
    args = parser.parse_args()
    if args.bot:
        run_bot()
    else:
        build_gui()


def main():
    cmd_parsing()

if __name__ == "__main__":
    main()