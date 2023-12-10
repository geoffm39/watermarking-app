from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from image_manager import ImageManager


class ThumbnailCanvas(Canvas):
    def __init__(self, parent, main_window, image_manager: ImageManager, **kwargs):
        super().__init__(parent, **kwargs)

        self.main_window = main_window
        self.image_manager = image_manager
        self.preview_mode = False

        self.thumbnail_frame = ttk.Frame(self)
        self.create_window(0, 0, anchor='nw', window=self.thumbnail_frame)

        self.thumbnail_menu = Menu(self.main_window.root, tearoff=0)
        self.thumbnail_menu.add_command(label='Rotate Right 90°', command=self.rotate_image_right)
        self.thumbnail_menu.add_command(label='Rotate Left 90°', command=self.rotate_image_left)
        self.thumbnail_menu.add_command(label='Remove', command=self.remove_image)
        # create a variable to hold the current focused thumbnail label when contextual menu accessed
        self.focused_label = None

    def set_preview_mode(self, is_preview_mode):
        self.preview_mode = is_preview_mode

    def add_preview_bindings(self):
        self.thumbnail_menu.delete(0, 2)
        self.thumbnail_menu.add_command(label='Remove', command=self.remove_image)
        for thumbnail_label in self.thumbnail_frame.winfo_children():
            thumbnail_label.bind('<Button-1>',
                                 lambda event: self.preview_thumbnail(event,
                                                                      self.main_window.preview_watermarked_image))

    def preview_thumbnail(self, event, main_window_function):
        x, y = self.winfo_pointerx(), self.winfo_pointery()
        self.focused_label = self.winfo_containing(x, y)
        main_window_function(self.focused_label.label_id)

    def show_image_menu(self, event):
        # set the current focused label when accessing the contextual menu
        x, y = self.winfo_pointerx(), self.winfo_pointery()
        self.focused_label = self.winfo_containing(x, y)

        self.thumbnail_menu.post(event.x_root, event.y_root)

    def rotate_image_left(self):
        self.image_manager.rotate_image_left(self.focused_label.label_id)
        self.update_thumbnails()
        self.focused_label = None

    def rotate_image_right(self):
        self.image_manager.rotate_image_right(self.focused_label.label_id)
        self.update_thumbnails()
        self.focused_label = None

    def remove_image(self):
        self.image_manager.remove_image(self.focused_label.label_id)
        self.update_thumbnails()
        self.focused_label = None

    def update_thumbnails(self):
        for thumbnail_label in self.thumbnail_frame.winfo_children():
            thumbnail_label.unbind('<Button-3>')
            thumbnail_label.destroy()
        for i, image in enumerate(self.image_manager.get_thumbnails()):
            thumbnail_label = ttk.Label(self.thumbnail_frame, image=image)
            thumbnail_label.grid(row=i // 5, column=i % 5, padx=5, pady=5)
            thumbnail_label.bind('<Button-3>', self.show_image_menu)
            thumbnail_label.label_id = i

        if self.preview_mode:
            self.add_preview_bindings()

        self.thumbnail_frame.update_idletasks()
        self.config(scrollregion=self.bbox('all'))
