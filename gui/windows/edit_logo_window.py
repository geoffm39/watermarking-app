from tkinter import *
from tkinter import ttk


class EditLogoWindow(Toplevel):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.title("Logo Editor")
        self.attributes('-topmost', 1)

        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)