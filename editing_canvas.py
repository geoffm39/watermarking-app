from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class EditingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

