from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class ThumbnailCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.thumbnail_frame = ttk.Frame(self)
        self.create_window(0, 0, anchor='nw', window=self.thumbnail_frame)

        self.images = []
        self.thumbnails = []

    def add_images(self, filepaths):
        for filepath in filepaths:
            image = Image.open(filepath)
            self.images.append(image)
            thumb_img = image.copy()
            thumb_img.thumbnail((200, 200))
            thumb_img = ImageTk.PhotoImage(thumb_img)
            self.thumbnails.append(thumb_img)
        self.update_thumbnails()

    def update_thumbnails(self):
        for thumbnail_label in self.thumbnail_frame.winfo_children():
            thumbnail_label.destroy()
        for i, image in enumerate(self.thumbnails):
            thumbnail_label = ttk.Label(self.thumbnail_frame, image=image)
            thumbnail_label.grid(row=i // 5, column=i % 5, padx=5, pady=5)
        self.thumbnail_frame.update_idletasks()
        self.config(scrollregion=self.bbox('all'))
