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
        self.root.iconbitmap('gui/images/watermark_icon.ico')
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

        # info view widgets
        self.info_canvas = Canvas(self.canvas_frame,
                                  width=1080,
                                  height=720)
        with Image.open('gui/images/app_background.jpg') as img:
            img.thumbnail((1080, 720))
            self.background_image = ImageTk.PhotoImage(img)
        self.select_files_button = ttk.Button(self.button_frame, text='Select Files', command=self.load_files)

        # thumbnail view widgets
        self.thumbnail_canvas = ThumbnailCanvas(self.canvas_frame,
                                                main_window=self,
                                                image_manager=self.image_manager,
                                                width=1080,
                                                height=654)
        self.canvas_scrollbar = ttk.Scrollbar(self.canvas_frame,
                                              orient='vertical',
                                              command=self.thumbnail_canvas.yview)
        self.thumbnail_canvas.configure(yscrollcommand=self.canvas_scrollbar.set)
        self.clear_files_button = ttk.Button(mainframe, text='Clear Files', command=self.clear_files)
        self.clear_files_button.configure(state='disabled')
        self.start_editing_button = ttk.Button(mainframe, text='Start Editing', command=self.start_editing)
        self.start_editing_button.configure(state='disabled')

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
        self.remove_button = ttk.Button(self.button_frame, text='Remove', command=self.remove_watermark)
        self.remove_button.configure(state='disabled')
        self.preview_watermarks_button = ttk.Button(mainframe,
                                                    text='Preview Watermarks',
                                                    command=self.preview_watermarks)
        self.preview_watermarks_button.configure(state='disabled')
        self.back_to_thumbs_button = ttk.Button(mainframe, text='Back', command=self.thumbnail_view)

        # preview view widgets
        self.save_images_button = ttk.Button(mainframe, text='Save Images', command=self.save_files)
        self.cancel_changes = ttk.Button(mainframe, text='Cancel Changes', command=self.cancel_changes)

        # preview image view widgets
        self.remove_image_button = ttk.Button(self.button_frame, text='Remove Image', command=self.remove_image)
        self.back_to_preview_button = ttk.Button(mainframe, text='Back', command=self.preview_view)

        # self.thumbnail_view()
        self.info_view()

    def load_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        self.image_manager.add_images(files)
        if self.image_manager.get_thumbnail_count() > 0:
            self.thumbnail_view()
            self.thumbnail_canvas.update_thumbnails()
            self.start_editing_button.configure(state='normal')
            self.clear_files_button.configure(state='normal')

    def clear_files(self):
        self.image_manager.remove_all_images()
        self.thumbnail_canvas.update_thumbnails()
        self.start_editing_button.configure(state='disabled')
        self.clear_files_button.configure(state='disabled')
        self.info_view()

    def save_files(self):
        folder = filedialog.askdirectory()
        self.image_manager.save_images(folder)
        self.root.destroy()

    def open_text_editor(self):
        self.text_editor_window = EditTextWindow(self.root,
                                                 image_manager=self.image_manager,
                                                 editing_canvas=self.editing_canvas,
                                                 main_window=self)

    def open_logo_editor(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file:
            self.image_manager.set_logo_image(file)
            self.logo_editor_window = EditLogoWindow(self.root,
                                                     image_manager=self.image_manager,
                                                     editing_canvas=self.editing_canvas,
                                                     main_window=self)

    def remove_watermark(self):
        self.image_manager.remove_watermark()
        self.add_text_button.configure(state='normal')
        self.add_logo_button.configure(state='normal')
        self.remove_button.configure(state='disabled')
        self.preview_watermarks_button.configure(state='disabled')
        self.editing_canvas.show_current_image()

    def preview_watermarks(self):
        self.image_manager.apply_watermarks()
        self.preview_view()

    def preview_watermarked_image(self, image_index):
        self.editing_canvas.set_image_index(image_index)
        self.preview_image_view()

    def cancel_changes(self):
        self.image_manager.cancel_image_changes()
        self.editing_view()

    def start_editing(self):
        self.editing_canvas.current_image_index = 0
        self.image_manager.set_current_image(self.editing_canvas.current_image_index)
        self.editing_view()

    def info_view(self):
        self.thumbnail_canvas.grid_forget()
        self.canvas_scrollbar.grid_forget()
        self.start_editing_button.grid_forget()
        self.clear_files_button.grid_forget()

        self.select_files_button.grid(column=0, row=0, padx=2)
        self.info_canvas.grid(column=0, row=0, sticky=(N, W, E, S))

        self.info_canvas.create_image(540, 360, image=self.background_image)
        info_box = self.info_canvas.create_rectangle((125, 125, 955, 595),
                                                     fill='white',
                                                     width=0)
        self.info_canvas.itemconfig(info_box, stipple='gray50')
        self.info_canvas.create_text((535, 360),
                                     text="Application for batch automatic watermarking of images\n\n\n"
                                          "Step 1: Select files to apply watermark to.\n\n"
                                          "Step 2: Right click on a thumbnail to remove or rotate the image.\n\n"
                                          "Step 3: Select 'Start Editing' and choose an image using the arrows to apply a watermark to.\n\n"
                                          "Step 4: Choose between a text or image watermark.\n\n"
                                          "Step 5: Edit the watermark and drag and drop to move, then select apply to complete.\n\n"
                                          "Step 6: Select 'Preview Watermarks' to view watermarked image thumbnails.\n\n"
                                          "Step 7: Left click a thumbnail to view enlarged image, or right click to remove.\n\n"
                                          "Step 8: When changes are complete select 'Save Images' to save watermarked images to chosen folder.\n\n\n"
                                          "For any further questions, bug reports or feedback, email me at geoffm39@gmail.com.  Thanks!",
                                     font=('Helvetica', '12', 'bold'))

    def thumbnail_view(self):
        self.editing_canvas.grid_forget()
        self.back_arrow_button.grid_forget()
        self.add_text_button.grid_forget()
        self.add_logo_button.grid_forget()
        self.remove_button.grid_forget()
        self.next_arrow_button.grid_forget()
        self.preview_watermarks_button.grid_forget()
        self.back_to_thumbs_button.grid_forget()

        self.select_files_button.grid(column=0, row=0, padx=2)
        self.clear_files_button.grid(column=0, row=0, sticky=W, padx=5)
        self.start_editing_button.grid(column=2, row=0, sticky=E, padx=5)

        self.thumbnail_canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.canvas_scrollbar.grid(column=1, row=0, sticky=(N, S))

        self.image_manager.remove_watermark()
        self.add_text_button.configure(state='normal')
        self.add_logo_button.configure(state='normal')
        self.remove_button.configure(state='disabled')
        self.preview_watermarks_button.configure(state='disabled')

        self.thumbnail_canvas.set_preview_mode(False)
        self.thumbnail_canvas.update_thumbnails()

    def editing_view(self):
        self.select_files_button.grid_forget()
        self.clear_files_button.grid_forget()
        self.start_editing_button.grid_forget()
        self.canvas_scrollbar.grid_forget()
        self.thumbnail_canvas.grid_forget()
        self.canvas_scrollbar.grid_forget()
        self.thumbnail_canvas.grid_forget()
        self.cancel_changes.grid_forget()
        self.save_images_button.grid_forget()

        self.editing_canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.back_arrow_button.grid(column=0, row=0, padx=2)
        self.add_text_button.grid(column=1, row=0, padx=2)
        self.add_logo_button.grid(column=2, row=0, padx=2)
        self.remove_button.grid(column=3, row=0, padx=2)
        self.next_arrow_button.grid(column=4, row=0, padx=2)
        self.preview_watermarks_button.grid(column=2, row=0, sticky=E, padx=5)
        self.back_to_thumbs_button.grid(column=0, row=0, sticky=W, padx=5)

        self.editing_canvas.show_current_image()

    def preview_view(self):
        self.editing_canvas.grid_forget()
        self.back_arrow_button.grid_forget()
        self.add_text_button.grid_forget()
        self.add_logo_button.grid_forget()
        self.remove_button.grid_forget()
        self.next_arrow_button.grid_forget()
        self.preview_watermarks_button.grid_forget()
        self.back_to_thumbs_button.grid_forget()
        self.back_to_preview_button.grid_forget()
        self.remove_image_button.grid_forget()

        self.cancel_changes.grid(column=0, row=0, sticky=W, padx=5)
        self.save_images_button.grid(column=2, row=0, sticky=E, padx=5)

        self.thumbnail_canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.canvas_scrollbar.grid(column=1, row=0, sticky=(N, S))

        self.image_manager.remove_watermark()
        self.remove_image_button.configure(state='normal')
        self.back_arrow_button.configure(state='normal')
        self.next_arrow_button.configure(state='normal')
        self.add_text_button.configure(state='normal')
        self.add_logo_button.configure(state='normal')
        self.remove_button.configure(state='disabled')
        self.preview_watermarks_button.configure(state='disabled')

        self.thumbnail_canvas.set_preview_mode(True)
        self.thumbnail_canvas.update_thumbnails()

    def preview_image_view(self):
        self.select_files_button.grid_forget()
        self.clear_files_button.grid_forget()
        self.start_editing_button.grid_forget()
        self.canvas_scrollbar.grid_forget()
        self.thumbnail_canvas.grid_forget()
        self.canvas_scrollbar.grid_forget()
        self.thumbnail_canvas.grid_forget()
        self.preview_watermarks_button.grid_forget()
        self.cancel_changes.grid_forget()

        self.editing_canvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.back_arrow_button.grid(column=0, row=0, padx=2)
        self.remove_image_button.grid(column=1, row=0, padx=2)
        self.next_arrow_button.grid(column=2, row=0, padx=2)
        self.back_to_preview_button.grid(column=0, row=0, sticky=W, padx=5)

        self.editing_canvas.show_current_image()

    def remove_image(self):
        self.image_manager.remove_image(self.editing_canvas.current_image_index)
        if self.image_manager.get_thumbnail_count() > 0:
            self.editing_canvas.set_image_index(0)
            self.editing_canvas.show_current_image()
        else:
            self.editing_canvas.delete('all')
            self.remove_image_button.configure(state='disabled')
            self.back_arrow_button.configure(state='disabled')
            self.next_arrow_button.configure(state='disabled')
