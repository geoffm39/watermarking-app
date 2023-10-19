import tkinter
from tkinter import *
from tkinter import ttk


class EditTextWindow(Toplevel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.title("Text Editor")
        self.attributes('-topmost', 1)

        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title_label = ttk.Label(mainframe, text='Text Properties')

        self.text = StringVar()
        self.text_entry = ttk.Entry(mainframe, textvariable=self.text)
        self.text_entry.insert(0, 'Enter Text Here')

        self.font = StringVar()
        self.font_combobox = ttk.Combobox(mainframe, textvariable=self.font)
        self.font_combobox.bind('<<ComboboxSelected>>', self.select_font)



        self.title_label.grid(column=0, row=0)
        self.text_entry.grid(column=0, row=1)
        self.font_combobox.grid(column=0, row=2)

    def select_font(self):
        pass
