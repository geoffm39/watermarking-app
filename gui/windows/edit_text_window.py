from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk

from image_manager import ImageManager
from font_manager import get_font_dict, get_font_names


class EditTextWindow(Toplevel):
    def __init__(self, root, image_manager: ImageManager, editing_canvas, **kwargs):
        super().__init__(root, **kwargs)
        self.title("Text Editor")
        self.attributes('-topmost', 1)

        self.image_manager = image_manager
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

        self.fonts_dict = get_font_dict()
        self.font = StringVar(value=get_font_names(self.fonts_dict)[0])
        self.font_path = self.fonts_dict[self.font.get()]
        self.font_combobox = ttk.Combobox(mainframe, textvariable=self.font)
        self.font_combobox.state(['readonly'])
        self.font_combobox['values'] = get_font_names(self.fonts_dict)
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
        self.text_image = Image.new('RGBA',
                                    self.image_manager.get_image(self.editing_canvas.current_image_index).size,
                                    (255, 255, 255, 0))
        fnt = ImageFont.truetype(self.font_path, 120)
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

    def test2(self):
        print(self.editing_canvas.coords(self.editing_canvas.canvas_image))
        print(self.editing_canvas.coords(self.editing_canvas.watermark))

        print(self.editing_canvas.bbox(self.editing_canvas.canvas_image))
        print(self.image_manager.get_current_image().size)

        canvas_x1, canvas_y1, canvas_x2, canvas_y2 = self.editing_canvas.bbox(self.editing_canvas.canvas_image)
        image_x_dim, image_y_dim = self.image_manager.get_image(self.editing_canvas.current_image_index).size
        x_ratio = image_x_dim / (canvas_x2 - canvas_x1)
        y_ratio = image_y_dim / (canvas_y2 - canvas_y1)

        image_x, image_y = self.editing_canvas.coords(self.editing_canvas.canvas_image)
        text_x, text_y = self.editing_canvas.coords(self.editing_canvas.watermark)

        watermark_x = int((text_x - image_x) * x_ratio)
        watermark_y = int((text_y - image_y) * y_ratio)

        image = self.image_manager.get_image(self.editing_canvas.current_image_index).convert('RGBA')
        image.alpha_composite(self.text_image, dest=(watermark_x, watermark_y))
        image.show()

        # WILL ALSO NEED TO ADJUST THE SIZE OF THE TEXT IMAGE BASED ON EACH IMAGE WHEN BATCH ADDING!!
        # CAN RESIZE THE TEXT IMAGE BASED ON THE RATIO OF DIFFERENCE FROM FIRST IMAGE TO EACH OTHER IMAGE

    def select_font(self, event):
        font_name = self.font.get()
        self.font_path = self.fonts_dict[font_name]

    def set_colour(self):
        colour = colorchooser.askcolor(parent=self)
        print(colour)  # returns a tuple with a tuple of the RGB and the hash code


    def toggle_tiles(self):
        pass  # enable and disable the tiled spacing scale
