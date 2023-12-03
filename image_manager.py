from PIL import Image, ImageTk, ImageDraw, ImageFont


class ImageManager:
    def __init__(self):
        # IMAGE LISTS
        self.images = []
        self.thumbnails = []

        # IMAGE OBJECTS
        self.current_editing_image = None
        self.current_editing_photo_image = None
        self.watermark = None
        self.logo_image = None
        self.logo_bg_mask = None

        # WATERMARK VARIABLES
        self.watermark_x_ratio = None
        self.watermark_y_ratio = None
        self.watermark_x_size_ratio = None
        self.watermark_y_size_ratio = None
        self.watermark_tile_spacing = 0
        self.watermark_spacing_ratio = None
        self.is_tiled = False

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

    def get_image(self, index):
        return self.images[index]

    def get_watermark(self):
        return self.watermark

    def set_current_image(self, index: int):
        image = self.images[index]
        editing_img = image.copy()
        editing_img.thumbnail((1080, 654))
        self.current_editing_image = editing_img
        self.current_editing_photo_image = ImageTk.PhotoImage(editing_img)

    def set_logo_image(self, filepath):
        with Image.open(filepath) as image:
            logo = image.convert('RGBA')
        width, height = logo.size

        # create a mask that identifies the background pixels
        self.logo_bg_mask = Image.new('L', (width, height), 0)

        # iterate through each pixel in the image and set mask pixel to 255 if not white
        for x in range(width):
            for y in range(height):
                pixel = logo.getpixel((x, y))
                if pixel[:3] != (255, 255, 255):
                    self.logo_bg_mask.putpixel((x, y), 255)

        self.logo_image = logo

    def set_logo_watermark(self, size_ratio, opacity, rotation, background, colour):
        watermark = self.logo_image.copy()
        mask = self.logo_bg_mask.copy()
        if colour:
            width, height = watermark.size
            for x in range(width):
                for y in range(height):
                    if mask.getpixel((x, y)) == 255:
                        watermark.putpixel((x, y), colour)
        if background:
            mask = mask.point(lambda p: opacity)
        else:
            mask = mask.point(lambda p: opacity if p == 255 else 0)
        watermark = watermark.rotate(rotation, expand=1, fillcolor=(255, 255, 255, 0))
        mask = mask.rotate(rotation, expand=1, fillcolor=0)
        watermark.putalpha(mask)
        alpha_channel = watermark.getchannel('A')
        bbox = alpha_channel.getbbox()
        watermark = watermark.crop(bbox)
        watermark = watermark.resize((int(watermark.width * size_ratio), int(watermark.height * size_ratio)))
        self.watermark = watermark
        photo_image = watermark.copy()
        photo_image.thumbnail((1080, 654))
        alpha_channel = photo_image.getchannel('A')
        bbox = alpha_channel.getbbox()
        photo_image = photo_image.crop(bbox)
        photo_image = ImageTk.PhotoImage(photo_image)
        return photo_image

    def set_text_watermark(self, index, text, font_path, font_size, rgb_values, outline, opacity, rotation):
        watermark = Image.new('RGBA',
                              self.get_image(index).size,
                              (255, 255, 255, 0))
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(watermark)
        r, g, b = rgb_values

        x = int(watermark.size[0] / 2)
        y = int(watermark.size[1] / 2)
        if outline:
            outline_width = 1  # Change this to the desired outline width
            for i in range(-outline_width, outline_width + 1):
                for j in range(-outline_width, outline_width + 1):
                    draw.text((x + i, y + j), text, font=font, fill=(0, 0, 0, opacity), anchor='mm')
            draw.text((x, y), text, font=font, fill=(r, g, b, opacity), anchor='mm')
        else:
            draw.text((x, y),
                      text=text,
                      font=font,
                      fill=(r, g, b, opacity),
                      anchor='mm')
        watermark = watermark.rotate(rotation)
        alpha_channel = watermark.getchannel('A')
        bbox = alpha_channel.getbbox()
        self.watermark = watermark.crop(bbox)
        photo_image = watermark.copy()
        photo_image.thumbnail((1080, 654))
        alpha_channel = photo_image.getchannel('A')
        bbox = alpha_channel.getbbox()
        watermark_photo_image = photo_image.crop(bbox)
        watermark_photo_image = ImageTk.PhotoImage(watermark_photo_image)
        return watermark_photo_image

    def set_watermark_ratios(self, x_ratio, y_ratio, x_size_ratio, y_size_ratio, spacing_ratio):
        self.watermark_x_ratio = x_ratio
        self.watermark_y_ratio = y_ratio
        self.watermark_x_size_ratio = x_size_ratio
        self.watermark_y_size_ratio = y_size_ratio
        self.watermark_spacing_ratio = spacing_ratio

    def set_tile_locations(self, image_x, image_y, watermark, start_x=0, start_y=0):
        tile_locations = []
        try:
            watermark_x = watermark.width()
            watermark_y = watermark.height()
        except TypeError:
            watermark_x, watermark_y = watermark.size
        rows = (image_y + watermark_y) // watermark_y
        columns = (image_x + watermark_x) // watermark_x
        x_increment = int(watermark_x + self.watermark_tile_spacing)
        y_increment = int(watermark_y + self.watermark_tile_spacing)
        for y in range(rows):
            row = []
            for x in range(columns):
                row.append((x * x_increment + start_x, y * y_increment + start_y))
            tile_locations.append(row)
        return tile_locations

    def set_tiled_bool(self, is_tiled):
        self.is_tiled = is_tiled

    def set_tile_spacing(self, spacing):
        self.watermark_tile_spacing = spacing

    def apply_watermarks(self):
        watermark = self.get_watermark().copy()
        watermark_x, watermark_y = watermark.size
        for i, image in enumerate(self.images):
            image = image.convert('RGBA')

            # set the new watermark width and height max values
            max_x = int(image.size[0] * self.watermark_x_size_ratio)
            max_y = int(image.size[1] * self.watermark_y_size_ratio)

            # calculate the width and height ratio difference and take the lowest value
            width_ratio = max_x / watermark_x
            height_ratio = max_y / watermark_y
            ratio = min(width_ratio, height_ratio)

            # set the new width and height using the ratio
            new_width = int(watermark_x * ratio)
            new_height = int(watermark_y * ratio)

            # call resize, passing in the new width and height
            watermark = watermark.resize((new_width, new_height))

            if self.is_tiled:
                self.set_tile_spacing(int(image.size[0] * self.watermark_spacing_ratio))
                locations = self.set_tile_locations(image_x=image.size[0], image_y=image.size[1], watermark=watermark)
                for row in locations:
                    for location in row:
                        image.alpha_composite(watermark, dest=(location[0], location[1]))

            else:
                image.alpha_composite(watermark, dest=(int(image.size[0] * self.watermark_x_ratio
                                                           - watermark.size[0] / 2),
                                                       int(image.size[1] * self.watermark_y_ratio
                                                           - watermark.size[1] / 2)))
            self.images[i] = image
            thumb = image.copy()
            thumb.thumbnail((200, 200))
            thumb = ImageTk.PhotoImage(thumb)
            self.thumbnails[i] = thumb

    def remove_watermark(self):
        self.watermark = None

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
