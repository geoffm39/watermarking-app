from tkinter import *

from image_manager import ImageManager


class EditingCanvas(Canvas):
    def __init__(self, parent, image_manager: ImageManager, **kwargs):
        super().__init__(parent, **kwargs)

        self.image_manager = image_manager
        self.editing_photo_image = None
        self.canvas_image = None
        self.current_image_index = 0

        self.watermark = None

        self.selected_image = None
        self.last_x = 540
        self.last_y = 327

    def set_image_index(self, image_index):
        self.current_image_index = image_index
        self.image_manager.set_current_image(self.current_image_index)
        self.show_current_image()

    def next_image_index(self):
        self.current_image_index += 1
        if self.current_image_index == self.image_manager.get_image_count():
            self.current_image_index = 0
        self.image_manager.set_current_image(self.current_image_index)
        self.show_current_image()

    def previous_image_index(self):
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = self.image_manager.get_image_count() - 1
        self.image_manager.set_current_image(self.current_image_index)
        self.show_current_image()

    def show_current_image(self):
        self.delete('all')
        if self.image_manager.get_current_photo_image() is None:
            self.image_manager.set_current_image(self.current_image_index)
        self.editing_photo_image = self.image_manager.get_current_photo_image()
        self.canvas_image = self.create_image(540, 327, image=self.editing_photo_image)
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

    def reset_image_location(self):
        self.last_x = 540
        self.last_y = 327
