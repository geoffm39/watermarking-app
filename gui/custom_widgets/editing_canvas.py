from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class EditingCanvas(Canvas):
    def __init__(self, parent, main_window, images, thumbnails, image_index, current_image,  **kwargs):
        super().__init__(parent, **kwargs)

        self.main_window = main_window
        self.images = images
        self.thumbnails = thumbnails
        self.current_image_index = image_index
        self.current_image = current_image
        self.current_photo_image = None

        self.selected_image = None
        self.last_x = 0
        self.last_y = 0
        self.watermark = None

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
        self.main_window.current_image = self.images[self.current_image_index]
        thumb_img = self.main_window.current_image.copy()
        thumb_img.thumbnail((1080, 654))
        self.current_photo_image = ImageTk.PhotoImage(thumb_img)
        self.create_image(540, 327, image=self.current_photo_image)

        self.update_idletasks()

    def on_image_press(self, event):
        image = self.find_closest(event.x, event.y)
        self.selected_image = image
        self.last_x, self.last_y = event.x, event.y

    def on_image_release(self, event):
        self.selected_image = None

    def on_image_drag(self, event):
        if self.selected_image:
            x, y = event.x, event.y
            x_delta = x - self.last_x
            y_delta = y - self.last_y
            self.move(self.selected_image, x_delta, y_delta)
            self.last_x, self.last_y = x, y
