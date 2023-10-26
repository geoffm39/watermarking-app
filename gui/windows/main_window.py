from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

from image_manager import ImageManager
from gui.custom_widgets.editing_canvas import EditingCanvas
from gui.custom_widgets.thumbnail_canvas import ThumbnailCanvas
from gui.windows.edit_text_window import EditTextWindow
from gui.windows.edit_logo_window import EditLogoWindow


class MainWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title('Watermark App')
        self.root.option_add('*tearOFF', FALSE)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.image_manager = ImageManager()

        self.text_editor_window = None
        self.logo_editor_window = None

        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(1, weight=1)

        self.images = []
        self.thumbnails = []
        self.current_image_index = 0
        self.current_image = None

        self.canvas_frame = ttk.Frame(mainframe, borderwidth=5, relief='ridge')
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.grid(column=0, row=1, columnspan=3, sticky=(N, W, E, S))

        self.button_frame = ttk.Frame(mainframe)
        self.button_frame.grid(column=1, row=0, pady=5, sticky=(W, E))

        # thumbnail view widgets
        self.thumbnail_canvas = ThumbnailCanvas(self.canvas_frame,
                                                root=self.root,
                                                image_manager=self.image_manager,
                                                width=1080,
                                                height=654)
        self.canvas_scrollbar = ttk.Scrollbar(self.canvas_frame,
                                              orient='vertical',
                                              command=self.thumbnail_canvas.yview)
        self.thumbnail_canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.select_files_button = ttk.Button(self.button_frame, text='Select Files', command=self.load_files)
        self.clear_files_button = ttk.Button(mainframe, text='Clear Files', command=self.clear_files)
        self.start_editing_button = ttk.Button(mainframe, text='Start Editing', command=self.editing_view)

        # editing view widgets
        self.editing_canvas = EditingCanvas(self.canvas_frame,
                                            image_manager=self.image_manager,
                                            width=1080,
                                            height=654)
        with Image.open('gui/images/next_arrow.png') as img:
            self.next_button_img = ImageTk.PhotoImage(img)
        with Image.open('gui/images/back_arrow.png') as img:
            self.back_button_img = ImageTk.PhotoImage(img)
        self.next_arrow_button = ttk.Button(self.button_frame,
                                            image=self.next_button_img,
                                            command=self.editing_canvas.next_image_index)
        self.back_arrow_button = ttk.Button(self.button_frame,
                                            image=self.back_button_img,
                                            command=self.editing_canvas.previous_image_index)
        self.add_text_button = ttk.Button(self.button_frame, text='Add Text', command=self.open_text_editor)
        self.add_logo_button = ttk.Button(self.button_frame, text='Add Logo', command=self.open_logo_editor)
        self.remove_button = ttk.Button(self.button_frame, text='Remove')
        self.add_watermarks_button = ttk.Button(mainframe, text='Apply Watermarks')
        self.back_to_thumbs_button = ttk.Button(mainframe, text='Back', command=self.thumbnail_view)

        self.thumbnail_view()

    def load_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        self.image_manager.add_images(files)
        self.thumbnail_canvas.update_thumbnails()

    def clear_files(self):
        self.image_manager.remove_all_images()
        self.thumbnail_canvas.update_thumbnails()

    def open_text_editor(self):
        self.text_editor_window = EditTextWindow(self.root,
                                                 image_manager=self.image_manager,
                                                 parent=self,
                                                 current_image=self.current_image,
                                                 editing_canvas=self.editing_canvas)

    def open_logo_editor(self):
        self.logo_editor_window = EditLogoWindow(self.root,
                                                 image_manager=self.image_manager)

    def thumbnail_view(self):
        self.editing_canvas.grid_forget()
        self.back_arrow_button.grid_forget()
        self.add_text_button.grid_forget()
        self.add_logo_button.grid_forget()
        self.remove_button.grid_forget()
        self.next_arrow_button.grid_forget()
        self.add_watermarks_button.grid_forget()
        self.back_to_thumbs_button.grid_forget()

        self.select_files_button.grid(column=0, row=0, padx=2)
        self.clear_files_button.grid(column=0, row=0, sticky=W, padx=5)
        self.start_editing_button.grid(column=2, row=0, sticky=E, padx=5)

        self.thumbnail_canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.canvas_scrollbar.grid(column=1, row=0, sticky=(N, S))

        self.thumbnail_canvas.update_thumbnails()

    def editing_view(self):
        self.select_files_button.grid_forget()
        self.clear_files_button.grid_forget()
        self.start_editing_button.grid_forget()
        self.canvas_scrollbar.grid_forget()
        self.thumbnail_canvas.grid_forget()
        self.canvas_scrollbar.grid_forget()
        self.thumbnail_canvas.grid_forget()

        self.editing_canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.back_arrow_button.grid(column=0, row=0, padx=2)
        self.add_text_button.grid(column=1, row=0, padx=2)
        self.add_logo_button.grid(column=2, row=0, padx=2)
        self.remove_button.grid(column=3, row=0, padx=2)
        self.next_arrow_button.grid(column=4, row=0, padx=2)
        self.add_watermarks_button.grid(column=2, row=0, sticky=E, padx=5)
        self.back_to_thumbs_button.grid(column=0, row=0, sticky=W, padx=5)

        self.editing_canvas.show_current_image()

