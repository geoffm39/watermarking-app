from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from gui.custom_widgets.thumbnail_canvas import ThumbnailCanvas
from gui.windows.edit_text_window import EditTextWindow
from gui.windows.edit_logo_window import EditLogoWindow

# SHOULD I MAKE TWO MODES USING FUNCTIONS?? ONE THUMBNAIL MODE (for thumbs and preview) AND ONE EDITING MODE
# for first editing, and individual editing in the preview mode

class MainWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title('Watermark App')
        self.root.option_add('*tearOFF', FALSE)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.images = []
        self.thumbnails = []

        # image thumbnail frame
        self.canvas_frame = ttk.Frame(mainframe, borderwidth=5, relief='ridge')
        self.thumbnail_canvas = ThumbnailCanvas(self.canvas_frame,
                                                root=self.root,
                                                images=self.images,
                                                thumbnails=self.thumbnails,
                                                width=1075,
                                                height=655)
        self.canvas_scrollbar = ttk.Scrollbar(self.canvas_frame,
                                              orient='vertical',
                                              command=self.thumbnail_canvas.yview)
        self.thumbnail_canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.thumbnail_canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.canvas_scrollbar.grid(column=1, row=0, sticky=(N, S))
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

        # centred button frame
        self.button_frame = ttk.Frame(mainframe)
        self.select_files_button = ttk.Button(self.button_frame, text='Select Files', command=self.load_files)
        self.select_files_button.grid(column=0, row=0, padx=2)

        self.clear_files_button = ttk.Button(mainframe, text='Clear Files',
                                             command=self.thumbnail_canvas.remove_all_images)
        self.start_editing_button = ttk.Button(mainframe, text='Start Editing')

        self.canvas_frame.grid(column=0, row=1, columnspan=3, sticky=(N, W, E, S))
        self.button_frame.grid(column=1, row=0, pady=5, sticky=(W, E))
        self.clear_files_button.grid(column=0, row=0, sticky=W, padx=5)
        self.start_editing_button.grid(column=2, row=0, sticky=E, padx=5)

        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(1, weight=1)

    def load_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        self.thumbnail_canvas.add_images(files)
