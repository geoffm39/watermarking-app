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
        self.resized_images = []
        self.current_image_index = 0
        self.image_label = None
        self.current_image = None

    def update_resized_images(self):
        self.resized_images = []
        for image in self.images:
            thumb_img = image.copy()
            thumb_img.thumbnail((1080, 655))
            thumb_img = ImageTk.PhotoImage(thumb_img)
            self.resized_images.append(thumb_img)

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
        if self.image_label:
            self.image_label.image = None
            self.image_label.destroy()
        self.image_label = ttk.Label(self.editing_frame, image=self.resized_images[self.current_image_index])
        self.image_label.grid(column=0, row=0, sticky=(N, W, E, S))

        self.editing_frame.update_idletasks()