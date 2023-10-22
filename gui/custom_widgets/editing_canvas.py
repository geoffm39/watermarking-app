from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class EditingCanvas(Canvas):
    def __init__(self, parent, images, thumbnails, image_index, current_image,  **kwargs):
        super().__init__(parent, **kwargs)

        self.images = images
        self.thumbnails = thumbnails
        self.current_image_index = image_index
        self.current_image = current_image

    def set_image_index(self, image_index):
        self.current_image_index = image_index
        self.show_current_image()

    def next_image_index(self):
        self.current_image_index += 1
        if self.current_image_index == len(self.images):
            self.current_image_index = 0
        self.show_current_image()

    def previous_image_index(self):
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.images) - 1
        self.show_current_image()

    def show_current_image(self):
        self.delete('all')
        self.current_image = self.images[self.current_image_index]
        thumb_img = self.current_image.copy()
        thumb_img.thumbnail((1080, 654))
        self.current_image = ImageTk.PhotoImage(thumb_img)
        self.create_image(540, 327, image=self.current_image)

        self.update_idletasks()