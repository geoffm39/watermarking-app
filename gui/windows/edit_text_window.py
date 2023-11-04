from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk

from gui.custom_widgets.editing_canvas import EditingCanvas
from image_manager import ImageManager
from font_manager import get_font_dict, get_font_names


class EditTextWindow(Toplevel):
    def __init__(self, root, image_manager: ImageManager, editing_canvas: EditingCanvas, **kwargs):
        super().__init__(root, **kwargs)
        self.title("Text Editor")
        self.attributes('-topmost', 1)

        self.image_manager = image_manager
        self.editing_canvas = editing_canvas

        self.text_photo_image = None

        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title_label = ttk.Label(mainframe, text='Text Properties')

        self.text = StringVar(value='Enter Text Here')
        self.text.trace_add('write', self.update_watermark)
        self.text_entry = ttk.Entry(mainframe, textvariable=self.text)

        self.fonts_dict = get_font_dict()
        self.font = StringVar(value=get_font_names(self.fonts_dict)[0])
        self.font_path = self.fonts_dict[self.font.get()]
        self.font_combobox = ttk.Combobox(mainframe, textvariable=self.font)
        self.font_combobox.state(['readonly'])
        self.font_combobox['values'] = get_font_names(self.fonts_dict)
        self.font_combobox.bind('<<ComboboxSelected>>', self.select_font)

        self.size = IntVar(value=50)
        self.size_scale = ttk.Scale(mainframe,
                                    orient=HORIZONTAL,
                                    variable=self.size,
                                    length=300,
                                    from_=1,
                                    to=1000,
                                    command=self.update_watermark)

        self.opacity = IntVar(value=128)
        self.opacity_scale = ttk.Scale(mainframe,
                                       orient=HORIZONTAL,
                                       variable=self.opacity,
                                       length=300,
                                       from_=0,
                                       to=255,
                                       command=self.update_watermark)

        self.rotation = IntVar(value=0)
        self.rotation_scale = ttk.Scale(mainframe,
                                        orient=HORIZONTAL,
                                        variable=self.rotation,
                                        length=300,
                                        from_=-180.0,
                                        to=180.0,
                                        command=self.update_watermark)

        self.colour = (255, 255, 255)
        self.colour_button = ttk.Button(mainframe,
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

        self.reset_button = ttk.Button(mainframe, text='Reset Watermark', command=self.reset_watermark)

        self.title_label.grid(column=0, row=0)
        self.text_entry.grid(column=0, row=1)
        self.font_combobox.grid(column=0, row=2)
        self.size_scale.grid(column=0, row=3)
        self.opacity_scale.grid(column=0, row=4)
        self.rotation_scale.grid(column=0, row=5)
        self.colour_button.grid(column=0, row=6)
        self.tiled_checkbutton.grid(column=0, row=7)
        self.tiled_spacing_scale.grid(column=0, row=8)
        self.reset_button.grid(column=0, row=9)

        self.update_watermark()

        self.apply_button = ttk.Button(mainframe, text='Apply Watermark', command=self.apply_watermark)
        self.apply_button.grid(column=0, row=10)

    def reset_watermark(self):
        self.size.set(50)
        self.opacity.set(128)
        self.rotation.set(0)
        self.colour = (255, 255, 255)
        self.text.set('Enter Text Here')
        self.editing_canvas.reset_image_location()
        self.update_watermark()

    def update_watermark(self, *args):
        self.text_photo_image = self.image_manager.set_text_watermark(
            index=self.editing_canvas.current_image_index,
            text=self.text.get(),
            font_path=self.font_path,
            font_size=self.size.get(),
            rgb_values=self.colour,
            opacity=self.opacity.get(),
            rotation=self.rotation.get())
        self.editing_canvas.watermark = self.editing_canvas.create_image(self.editing_canvas.last_x,
                                                                         self.editing_canvas.last_y,
                                                                         image=self.text_photo_image)

        self.editing_canvas.tag_bind(self.editing_canvas.watermark, "<ButtonPress-1>",
                                     self.editing_canvas.on_image_press)
        self.editing_canvas.tag_bind(self.editing_canvas.watermark, "<ButtonRelease-1>",
                                     self.editing_canvas.on_image_release)
        self.editing_canvas.tag_bind(self.editing_canvas.watermark, "<B1-Motion>", self.editing_canvas.on_image_drag)
        self.editing_canvas.update_idletasks()

    def apply_watermark(self):
        # calculate the ratio size difference from original image on x and y axes
        canvas_x1, canvas_y1, canvas_x2, canvas_y2 = self.editing_canvas.bbox(self.editing_canvas.canvas_image)
        image_x_dim, image_y_dim = self.image_manager.get_image(self.editing_canvas.current_image_index).size
        x_ratio = image_x_dim / (canvas_x2 - canvas_x1)
        y_ratio = image_y_dim / (canvas_y2 - canvas_y1)

        # calculate the x and y locations of the watermark on the original image
        text_x1, text_y1, text_x2, text_y2 = self.editing_canvas.bbox(self.editing_canvas.watermark)
        watermark_x = int((text_x1 - canvas_x1) * x_ratio)
        watermark_y = int((text_y1 - canvas_y1) * y_ratio)

        # WHAT IF THE WATERMARK IS ROTATED!! THE SIZE RATIO WILL BE DIFFERENT DUE TO CALCULATION ALONG X AXIS

        self.image_manager.set_watermark_ratios(x_ratio=watermark_x / image_x_dim,
                                                y_ratio=watermark_y / image_y_dim,
                                                size_ratio=self.image_manager.get_watermark().size[0] / image_x_dim)

        # image = self.image_manager.get_image(self.editing_canvas.current_image_index).convert('RGBA')
        # image.alpha_composite(self.image_manager.get_watermark(), dest=(watermark_x, watermark_y))
        # image.show()

    def select_font(self, event):
        font_name = self.font.get()
        self.font_path = self.fonts_dict[font_name]
        self.update_watermark()

    def set_colour(self):
        colour = colorchooser.askcolor(parent=self)
        self.colour = colour[0]
        self.update_watermark()

    def toggle_tiles(self):
        pass  # enable and disable the tiled spacing scale
