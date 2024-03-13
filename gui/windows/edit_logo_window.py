from tkinter import *
from tkinter import ttk
from tkinter import colorchooser

from gui.custom_widgets.editing_canvas import EditingCanvas
from image_manager import ImageManager


class EditLogoWindow(Toplevel):
    def __init__(self, root, image_manager: ImageManager, editing_canvas: EditingCanvas, main_window, **kwargs):
        super().__init__(root, **kwargs)
        self.title("Logo Editor")
        self.attributes('-topmost', 1)
        self.resizable(FALSE, FALSE)
        self.protocol('WM_DELETE_WINDOW', self.window_closed)

        self.image_manager = image_manager
        self.editing_canvas = editing_canvas
        self.main_window = main_window

        self.logo_photo_image = None

        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title_label = ttk.Label(mainframe, text='Logo Properties', anchor='center')

        self.size_label = ttk.Label(mainframe, text='Size')
        self.size = DoubleVar(value=1)
        self.size_scale = ttk.Scale(mainframe,
                                    orient=HORIZONTAL,
                                    variable=self.size,
                                    length=300,
                                    from_=0.05,
                                    to=10,
                                    command=self.update_canvas)

        self.opacity_label = ttk.Label(mainframe, text='Opacity')
        self.opacity = IntVar(value=128)
        self.opacity_scale = ttk.Scale(mainframe,
                                       orient=HORIZONTAL,
                                       variable=self.opacity,
                                       length=300,
                                       from_=0,
                                       to=255,
                                       command=self.update_canvas)

        self.rotation_label = ttk.Label(mainframe, text='Rotation')
        self.rotation = IntVar(value=0)
        self.rotation_scale = ttk.Scale(mainframe,
                                        orient=HORIZONTAL,
                                        variable=self.rotation,
                                        length=300,
                                        from_=-180.0,
                                        to=180.0,
                                        command=self.update_canvas)

        self.colour_label = ttk.Label(mainframe, text='Colour')
        self.colour = (255, 255, 255)
        colour_frame = ttk.Frame(mainframe)
        self.background = BooleanVar(value=True)
        self.background_checkbutton = ttk.Checkbutton(colour_frame,
                                                      text='Background',
                                                      variable=self.background,
                                                      command=self.update_canvas,
                                                      onvalue=True,
                                                      offvalue=False)
        self.colour = None
        self.colour_button = ttk.Button(colour_frame,
                                        text='Colour',
                                        command=self.set_colour)

        self.tiled = BooleanVar()
        self.tiled_checkbutton = ttk.Checkbutton(mainframe,
                                                 text='Tiled',
                                                 variable=self.tiled,
                                                 command=self.update_canvas,
                                                 onvalue=True,
                                                 offvalue=False)
        spacing_frame = ttk.Frame(mainframe)
        self.spacing_label = ttk.Label(spacing_frame, text='Spacing')
        self.tiled_spacing = IntVar(value=0)
        self.tiled_spacing_scale = ttk.Scale(spacing_frame,
                                             orient=HORIZONTAL,
                                             variable=self.tiled_spacing,
                                             command=self.set_tile_spacing,
                                             length=245,
                                             from_=0,
                                             to=300.0)
        self.tiled_spacing_scale.configure(state='disabled')

        self.reset_button = ttk.Button(mainframe, text='Reset', command=self.reset_watermark)
        self.apply_button = ttk.Button(mainframe, text='Apply', command=self.apply_watermark)

        self.title_label.grid(column=0, row=0, columnspan=2, sticky=(W, E), pady=(5, 0))
        self.s1 = ttk.Separator(mainframe, orient=HORIZONTAL)
        self.s1.grid(column=0, row=1, columnspan=2, sticky=(W, E), padx=10, pady=5)
        self.size_label.grid(column=0, row=2, sticky=W, padx=10)
        self.size_scale.grid(column=1, row=2, padx=(0, 10))
        self.s2 = ttk.Separator(mainframe, orient=HORIZONTAL)
        self.s2.grid(column=0, row=3, columnspan=2, sticky=(W, E), padx=10, pady=5)
        self.opacity_label.grid(column=0, row=4, sticky=W, padx=10)
        self.opacity_scale.grid(column=1, row=4, padx=(0, 10))
        self.s3 = ttk.Separator(mainframe, orient=HORIZONTAL)
        self.s3.grid(column=0, row=5, columnspan=2, sticky=(W, E), padx=10, pady=5)
        self.rotation_label.grid(column=0, row=6, sticky=W, padx=10)
        self.rotation_scale.grid(column=1, row=6, padx=(0, 10))
        self.s4 = ttk.Separator(mainframe, orient=HORIZONTAL)
        self.s4.grid(column=0, row=7, columnspan=2, sticky=(W, E), padx=10, pady=5)
        self.colour_label.grid(column=0, row=8, sticky=W, padx=10)
        colour_frame.grid(column=1, row=8)
        self.colour_button.grid(column=0, row=0, padx=(0, 20))
        self.background_checkbutton.grid(column=1, row=0, padx=(20, 0))
        self.s5 = ttk.Separator(mainframe, orient=HORIZONTAL)
        self.s5.grid(column=0, row=9, columnspan=2, sticky=(W, E), padx=10, pady=5)
        self.tiled_checkbutton.grid(column=0, row=10, sticky=W, padx=10)
        spacing_frame.grid(column=1, row=10)
        self.spacing_label.grid(column=0, row=0, sticky=W)
        self.tiled_spacing_scale.grid(column=1, row=0, padx=10)
        self.s6 = ttk.Separator(mainframe, orient=HORIZONTAL)
        self.s6.grid(column=0, row=11, columnspan=2, sticky=(W, E), padx=10, pady=5)
        self.reset_button.grid(column=0, row=12, sticky=W, padx=(10, 0), pady=(0, 5))
        self.apply_button.grid(column=1, row=12, sticky=E, padx=(0, 10), pady=(0, 5))

        self.reset_watermark()
        self.update_canvas()

    def reset_watermark(self):
        self.size.set(1)
        self.opacity.set(128)
        self.rotation.set(0)
        self.tiled.set(False)
        self.tiled_spacing.set(0)
        self.editing_canvas.reset_image_location()
        self.update_canvas()

    def update_canvas(self, *args):
        if self.tiled.get():
            self.update_watermark_tiles()
        else:
            self.update_watermark()

    def update_watermark(self, *args):
        self.image_manager.set_tiled_bool(self.tiled.get())
        self.tiled_spacing_scale.configure(state='disabled')
        self.logo_photo_image = self.image_manager.set_logo_watermark(size_ratio=self.size.get(),
                                                                      opacity=self.opacity.get(),
                                                                      rotation=self.rotation.get(),
                                                                      background=self.background.get(),
                                                                      colour=self.colour)
        self.editing_canvas.watermark = self.editing_canvas.create_image(self.editing_canvas.last_x,
                                                                         self.editing_canvas.last_y,
                                                                         image=self.logo_photo_image)

        self.editing_canvas.tag_bind(self.editing_canvas.watermark, "<ButtonPress-1>",
                                     self.editing_canvas.on_image_press)
        self.editing_canvas.tag_bind(self.editing_canvas.watermark, "<ButtonRelease-1>",
                                     self.editing_canvas.on_image_release)
        self.editing_canvas.tag_bind(self.editing_canvas.watermark, "<B1-Motion>", self.editing_canvas.on_image_drag)
        self.editing_canvas.update_idletasks()

    def update_watermark_tiles(self):
        self.image_manager.set_tiled_bool(self.tiled.get())
        self.tiled_spacing_scale.configure(state='normal')
        self.editing_canvas.show_current_image()
        self.logo_photo_image = self.image_manager.set_logo_watermark(size_ratio=self.size.get(),
                                                                      opacity=self.opacity.get(),
                                                                      rotation=self.rotation.get(),
                                                                      background=self.background.get(),
                                                                      colour=self.colour)

        # set tile locations based on thumbnail size
        canvas_x1, canvas_y1, canvas_x2, canvas_y2 = self.editing_canvas.bbox(self.editing_canvas.canvas_image)
        locations = self.image_manager.set_tile_locations(image_x=canvas_x2 - canvas_x1,
                                                          image_y=canvas_y2 - canvas_y1,
                                                          watermark=self.logo_photo_image,
                                                          start_x=canvas_x1,
                                                          start_y=canvas_y1)

        for row in locations:
            for location in row:
                self.editing_canvas.watermark = self.editing_canvas.create_image(int(location[0] +
                                                                                     self.logo_photo_image.width()
                                                                                     / 2),
                                                                                 int(location[1] +
                                                                                     self.logo_photo_image.height()
                                                                                     / 2),
                                                                                 image=self.logo_photo_image)
        self.editing_canvas.update_idletasks()

    def apply_watermark(self):
        # calculate the ratio size difference from original image on x and y axes
        canvas_x1, canvas_y1, canvas_x2, canvas_y2 = self.editing_canvas.bbox(self.editing_canvas.canvas_image)
        image_x_dim, image_y_dim = self.image_manager.get_image(self.editing_canvas.current_image_index).size
        x_ratio = image_x_dim / (canvas_x2 - canvas_x1)
        y_ratio = image_y_dim / (canvas_y2 - canvas_y1)

        # calculate the centred x and y locations of the watermark on the original image
        text_x1, text_y1, text_x2, text_y2 = self.editing_canvas.bbox(self.editing_canvas.watermark)
        watermark_x = int((text_x1 + (text_x2 - text_x1) / 2 - canvas_x1) * x_ratio)
        watermark_y = int((text_y1 + (text_y2 - text_y1) / 2 - canvas_y1) * y_ratio)

        self.image_manager.set_watermark_ratios(x_ratio=watermark_x / image_x_dim,
                                                y_ratio=watermark_y / image_y_dim,
                                                x_size_ratio=(text_x2 - text_x1) / (canvas_x2 - canvas_x1),
                                                y_size_ratio=(text_y2 - text_y1) / (canvas_y2 - canvas_y1),
                                                spacing_ratio=self.tiled_spacing.get() * x_ratio / image_x_dim)

        # unbind the watermark bindings to stop drag and drop after applying
        self.editing_canvas.tag_unbind(self.editing_canvas.watermark, '<ButtonPress-1>')
        self.editing_canvas.tag_unbind(self.editing_canvas.watermark, '<ButtonRelease-1>')
        self.editing_canvas.tag_unbind(self.editing_canvas.watermark, '<B1-Motion>')

        self.main_window.add_text_button.configure(state='disabled')
        self.main_window.add_logo_button.configure(state='disabled')
        self.main_window.remove_button.configure(state='normal')
        self.main_window.preview_watermarks_button.configure(state='normal')
        self.destroy()

    def set_colour(self):
        colour = colorchooser.askcolor(parent=self)
        self.colour = colour[0]
        self.update_canvas()

    def set_tile_spacing(self, *args):
        self.image_manager.set_tile_spacing(self.tiled_spacing.get())
        self.update_canvas()

    def window_closed(self):
        self.image_manager.remove_watermark()
        self.editing_canvas.show_current_image()
        self.destroy()