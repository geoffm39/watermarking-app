from PIL import Image, ImageTk, ImageDraw, ImageFont


class ImageManager:
    def __init__(self):
        self.images = []
        self.thumbnails = []

        self.current_editing_thumb = None

        self.text_watermarks = []
        self.logo_watermarks = []

        # would it be better to have a dictionary rather than multiple lists?
        # should the file path also be here?

    def add_images(self, filepaths):
        for filepath in filepaths:
            with Image.open(filepath) as image:
                self.images.append(image)
                thumb_img = image.copy()
            thumb_img.thumbnail((200, 200))
            thumb_img = ImageTk.PhotoImage(thumb_img)
            self.thumbnails.append(thumb_img)

    def get_thumbnails(self):
        return self.thumbnails

    def get_image_count(self):
        return len(self.images)

    def set_editing_thumbnail(self, index: int):
        image = self.images[index]
        editing_img = image.copy()
        editing_img.thumbnail((1080, 654))
        self.current_editing_thumb = ImageTk.PhotoImage(editing_img)

    def get_editing_thumbnail(self):
        return self.current_editing_thumb

    def remove_all_images(self):
        self.images = []
        self.thumbnails = []

    def remove_image(self, index):
        self.images.pop(index)
        self.thumbnails.pop(index)

    def rotate_image_left(self, index):
        image = self.images[index]
        rotated_img = image.transpose(Image.Transpose.ROTATE_90)
        self.images[index] = rotated_img
        rotated_thumb = rotated_img.copy()
        rotated_thumb.thumbnail((200, 200))
        rotated_thumb = ImageTk.PhotoImage(rotated_thumb)
        self.thumbnails[index] = rotated_thumb

    def rotate_image_right(self, index):
        image = self.images[index]
        rotated_img = image.transpose(Image.Transpose.ROTATE_270)
        self.images[index] = rotated_img
        rotated_thumb = rotated_img.copy()
        rotated_thumb.thumbnail((200, 200))
        rotated_thumb = ImageTk.PhotoImage(rotated_thumb)
        self.thumbnails[index] = rotated_thumb

