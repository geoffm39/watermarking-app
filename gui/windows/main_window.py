from tkinter import *
from tkinter import ttk
from gui.windows.edit_text_window import EditTextWindow
from gui.windows.edit_logo_window import EditLogoWindow
class MainWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title('Watermark App')

        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
