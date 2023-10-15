from tkinter import *
from tkinter import ttk

class EditLogoWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Logo Editor")