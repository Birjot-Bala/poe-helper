# poe_helper.py

from gui import Gui

def build_gui():
    gui = Gui()

    gui.master.title('POE Helper')
    gui.master.resizable(False,False)
    gui.master.minsize(200,100)
    gui.master.grid_columnconfigure(0, weight=1)

    gui.mainloop()


def main():
    build_gui()


if __name__ == "__main__":
    main()