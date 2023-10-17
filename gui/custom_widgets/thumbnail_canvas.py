from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class ThumbnailCanvas(Canvas):
    def __init__(self, parent, root, images, thumbnails, **kwargs):
        super().__init__(parent, **kwargs)

        self.root = root
        self.thumbnail_frame = ttk.Frame(self)
        self.create_window(0, 0, anchor='nw', window=self.thumbnail_frame)

        self.images = images
        self.thumbnails = thumbnails

        self.thumbnail_menu = Menu(self.root, tearoff=0)
        self.thumbnail_menu.add_command(label='Rotate Right 90°', command=self.rotate_image_right)
        self.thumbnail_menu.add_command(label='Rotate Left 90°', command=self.rotate_image_left)
        self.thumbnail_menu.add_command(label='Remove', command=self.remove_image)
        # create a variable to hold the current focused thumbnail label when contextual menu accessed
        self.focused_label = None

    def show_image_menu(self, event):
        # set the current focused label when accessing the contextual menu
        x, y = self.winfo_pointerx(), self.winfo_pointery()
        self.focused_label = self.winfo_containing(x, y)

        self.thumbnail_menu.post(event.x_root, event.y_root)

    def rotate_image_left(self):
        image = self.images[self.focused_label.label_id]
        rotated_img = image.transpose(Image.Transpose.ROTATE_90)
        self.images[self.focused_label.label_id] = rotated_img
        rotated_thumb = rotated_img.copy()
        rotated_thumb.thumbnail((200, 200))
        rotated_thumb = ImageTk.PhotoImage(rotated_thumb)
        self.thumbnails[self.focused_label.label_id] = rotated_thumb
        self.update_thumbnails()
        self.focused_label = None

    def rotate_image_right(self):
        image = self.images[self.focused_label.label_id]
        rotated_img = image.transpose(Image.Transpose.ROTATE_270)
        self.images[self.focused_label.label_id] = rotated_img
        rotated_thumb = rotated_img.copy()
        rotated_thumb.thumbnail((200, 200))
        rotated_thumb = ImageTk.PhotoImage(rotated_thumb)
        self.thumbnails[self.focused_label.label_id] = rotated_thumb
        self.update_thumbnails()
        self.focused_label = None

    def remove_image(self):
        self.images.pop(self.focused_label.label_id)
        self.thumbnails.pop(self.focused_label.label_id)
        self.update_thumbnails()
        self.focused_label = None

    def remove_all_images(self):
        self.images = []
        self.thumbnails = []
        self.update_thumbnails()

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
            thumbnail_label.unbind('<Button-3>')
            thumbnail_label.destroy()
        for i, image in enumerate(self.thumbnails):
            thumbnail_label = ttk.Label(self.thumbnail_frame, image=image)
            thumbnail_label.grid(row=i // 5, column=i % 5, padx=5, pady=5)
            thumbnail_label.bind('<Button-3>', self.show_image_menu)
            thumbnail_label.label_id = i

        self.thumbnail_frame.update_idletasks()
        self.config(scrollregion=self.bbox('all'))
