from PIL import Image, ImageTk, ImageDraw, ImageFont


class ImageManager:
    def __init__(self):
        self.images = []
        self.thumbnails = []

        self.current_editing_image = None
        self.current_editing_photo_image = None
        self.current_text_image = None
        self.current_text_photo_image = None

        self.text_watermarks = []
        self.logo_watermarks = []

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

    def get_current_photo_image(self):
        return self.current_editing_photo_image

    def get_current_image(self):
        return self.current_editing_image

    def get_image(self, index):
        return self.images[index]

    def create_text_watermark(self, index, text, font_path, font_size, rgb_values, opacity, rotation):
        watermark = Image.new('RGBA',
                              self.get_image(index).size,
                              (255, 255, 255, 0))
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(watermark)
        r, g, b = rgb_values
        draw.text((int(watermark.size[0] / 2), int(watermark.size[1] / 2)),
                  text=text,
                  font=font,
                  fill=(r, g, b, opacity),
                  anchor='mm')
        watermark = watermark.rotate(rotation)
        alpha_channel = watermark.getchannel('A')
        bbox = alpha_channel.getbbox()
        self.current_text_image = watermark.crop(bbox)
        photo_image = watermark.copy()
        photo_image.thumbnail((1080, 654))
        alpha_channel = photo_image.getchannel('A')
        bbox = alpha_channel.getbbox()
        self.current_text_photo_image = photo_image.crop(bbox)
        self.current_text_photo_image = ImageTk.PhotoImage(self.current_text_photo_image)
        return self.current_text_image, self.current_text_photo_image

    def set_current_image(self, index: int):
        image = self.images[index]
        editing_img = image.copy()
        editing_img.thumbnail((1080, 654))
        self.current_editing_image = editing_img
        self.current_editing_photo_image = ImageTk.PhotoImage(editing_img)

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
