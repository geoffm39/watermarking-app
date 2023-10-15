from tkinter import *
from tkinter import ttk

class EditTextWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Text Editor")