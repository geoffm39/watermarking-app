from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class EditingCanvas(Canvas):
    def __init__(self, parent, images, thumbnails,  **kwargs):
        super().__init__(parent, **kwargs)

        self.editing_frame = ttk.Frame(self)
        self.create_window(0, 0, anchor='nw', window=self.editing_frame)

        self.images = images
        self.thumbnails = thumbnails
