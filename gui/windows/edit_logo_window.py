from tkinter import *
from tkinter import ttk

from image_manager import ImageManager


class EditLogoWindow(Toplevel):
    def __init__(self, root, image_manager: ImageManager, **kwargs):
        super().__init__(root, **kwargs)
        self.title("Logo Editor")
        self.attributes('-topmost', 1)

        self.image_manager = image_manager

        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)