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
        self.current_image_index = None
        self.image_label = None

        # SHOULD I CREATE ANOTHER LIST WITH EDITING IMAGES SETTING A LARGE THUMBNAIL TO KEEP SAME SIZE??
        # if i do this how can i set the wanted position of the text and logo with dragging around???
        # need to apply the text and logos to a percentage location and size relevent to thumbnail for each image

        # THE SCROLLING WILL MOVE THESE! disable these buttons after picking first image to edit
        # if these move around the screen as changing images, just remove them! (add buttons up top instead)
        with Image.open('gui/images/next_arrow.png') as img:
            self.next_button_img = ImageTk.PhotoImage(img)
        with Image.open('gui/images/back_arrow.png') as img:
            self.back_button_img = ImageTk.PhotoImage(img)
        self.next_arrow_button = ttk.Button(self.editing_frame, image=self.next_button_img)
        self.back_arrow_button = ttk.Button(self.editing_frame, image=self.back_button_img)

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
            self.image_label.destroy()
        tk_version = ImageTk.PhotoImage(self.images[self.current_image_index])
        self.image_label = ttk.Label(self.editing_frame, image=tk_version)
        self.image_label.grid()
