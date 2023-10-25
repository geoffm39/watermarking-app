from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk

from image_manager import ImageManager


class EditTextWindow(Toplevel):
    def __init__(self, root, image_manager: ImageManager, parent, current_image, editing_canvas, **kwargs):
        super().__init__(root, **kwargs)
        self.title("Text Editor")
        self.attributes('-topmost', 1)

        self.image_manager = image_manager

        self.parent = parent
        self.current_image = current_image
        self.editing_canvas = editing_canvas
        self.text_photo_image = None
        self.text_image = None

        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title_label = ttk.Label(mainframe, text='Text Properties')

        self.text = StringVar(value='Enter Text Here')
        self.text_entry = ttk.Entry(mainframe, textvariable=self.text)

        self.font = StringVar()
        self.font_combobox = ttk.Combobox(mainframe, textvariable=self.font)
        self.font_combobox.bind('<<ComboboxSelected>>', self.select_font)

        self.size = DoubleVar()
        self.size_scale = ttk.Scale(mainframe,
                                    orient=HORIZONTAL,
                                    variable=self.size,
                                    length=300,
                                    from_=1.0,
                                    to=100.0)

        self.opacity = DoubleVar()
        self.opacity_scale = ttk.Scale(mainframe,
                                       orient=HORIZONTAL,
                                       variable=self.opacity,
                                       length=300,
                                       from_=1.0,
                                       to=100.0)

        self.rotation = DoubleVar()
        self.rotation_scale = ttk.Scale(mainframe,
                                        orient=HORIZONTAL,
                                        variable=self.rotation,
                                        length=300,
                                        from_=-180.0,
                                        to=180.0)

        self.color_button = ttk.Button(mainframe,
                                       text='Colour',
                                       command=self.set_colour)

        self.tiled = BooleanVar()
        self.tiled_checkbutton = ttk.Checkbutton(mainframe,
                                                 text='Tiled',
                                                 variable=self.tiled,
                                                 command=self.toggle_tiles,
                                                 onvalue=True,
                                                 offvalue=False)
        self.tiled_spacing = DoubleVar()
        self.tiled_spacing_scale = ttk.Scale(mainframe,
                                             orient=HORIZONTAL,
                                             variable=self.tiled_spacing,
                                             length=200,
                                             from_=1.0,
                                             to=100.0)

        self.title_label.grid(column=0, row=0)
        self.text_entry.grid(column=0, row=1)
        self.font_combobox.grid(column=0, row=2)
        self.size_scale.grid(column=0, row=3)
        self.opacity_scale.grid(column=0, row=4)
        self.rotation_scale.grid(column=0, row=5)
        self.color_button.grid(column=0, row=6)
        self.tiled_checkbutton.grid(column=0, row=7)
        self.tiled_spacing_scale.grid(column=0, row=8)

        # TESTING BUTTON
        self.test_button = ttk.Button(mainframe, text='test', command=self.test)
        self.test_button.grid(column=0, row=9)
        self.test2_button = ttk.Button(mainframe, text='test2', command=self.test2)
        self.test2_button.grid(column=0, row=10)

    def test(self):
        # then create a thumbnail of that image after adding the text
        # then add that image to the canvas
        self.text_image = Image.new('RGBA', self.parent.current_image.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype("fonts/aspire.ttf", 120)
        d = ImageDraw.Draw(self.text_image)
        d.text((10, 10), "Hello", font=fnt, fill=(255, 255, 255, 128))
        # draw text, full opacity
        d.text((10, 60), "World", font=fnt, fill=(255, 255, 255, 255))
        self.text_photo_image = self.text_image.copy()
        self.text_photo_image.thumbnail((1080, 654))
        self.text_photo_image = ImageTk.PhotoImage(self.text_photo_image)
        self.editing_canvas.watermark = self.editing_canvas.create_image(540, 327, image=self.text_photo_image)

        self.editing_canvas.tag_bind(self.editing_canvas.watermark, "<ButtonPress-1>", self.editing_canvas.on_image_press)
        self.editing_canvas.tag_bind(self.editing_canvas.watermark, "<ButtonRelease-1>", self.editing_canvas.on_image_release)
        self.editing_canvas.tag_bind(self.editing_canvas.watermark, "<B1-Motion>", self.editing_canvas.on_image_drag)
        self.editing_canvas.update_idletasks()

        self.parent.current_image = self.parent.current_image.convert('RGBA')
        self.parent.current_image.alpha_composite(self.text_image, dest=(2450, 500))
        self.parent.current_image.show()

    def test2(self):
        # THIS NOT RETURNING ANY TUPLE
        print(self.editing_canvas.coords(self.editing_canvas.current_photo_image))
        print(self.editing_canvas.coords(self.text_photo_image))

    def select_font(self):
        pass

    def set_colour(self):
        colour = colorchooser.askcolor(parent=self)
        print(colour)  # returns a tuple with a tuple of the RGB and the hash code


    def toggle_tiles(self):
        pass  # enable and disable the tiled spacing scale
