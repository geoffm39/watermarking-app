from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from image_manager import ImageManager


class EditingCanvas(Canvas):
    def __init__(self, parent, image_manager: ImageManager, **kwargs):
        super().__init__(parent, **kwargs)

        self.image_manager = image_manager
        self.editing_thumbnail = None
        self.current_image_index = 0

        self.selected_image = None
        self.last_x = 0
        self.last_y = 0

    def set_image_index(self, image_index):
        self.current_image_index = image_index
        self.image_manager.set_editing_thumbnail(self.current_image_index)
        self.show_current_image()

    def next_image_index(self):
        self.current_image_index += 1
        if self.current_image_index == self.image_manager.get_image_count():
            self.current_image_index = 0
        self.image_manager.set_editing_thumbnail(self.current_image_index)
        self.show_current_image()

    def previous_image_index(self):
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = self.image_manager.get_image_count() - 1
        self.image_manager.set_editing_thumbnail(self.current_image_index)
        self.show_current_image()

    def show_current_image(self):
        self.delete('all')
        if self.image_manager.get_editing_thumbnail() is None:
            self.image_manager.set_editing_thumbnail(self.current_image_index)
        self.editing_thumbnail = self.image_manager.get_editing_thumbnail()
        self.create_image(540, 327, image=self.editing_thumbnail)
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

            # BUT THIS WORKS
            print(self.coords(self.selected_image))
