import tkinter as tk
import guifunc
from config import config, Settings


class Toolbar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent: ImageViewer = parent

        self.prev_button = tk.Button(self, text="<", command=self.decrement_page)
        self.next_button = tk.Button(self, text=">", command=self.increment_page)
        self.aa_enable = tk.Checkbutton(self, text="anti alias", command=self.button_checked)
        self.aa_enable.select()

        self.prev_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.LEFT)
        self.aa_enable.pack()

    def increment_page(self, *args) -> None:
        """
        Calls the increment_page function with a value of 1. This will
        add one to the current page and then display that page.
        """
        guifunc.increment_page(self.parent, 1)

    def decrement_page(self, *args) -> None:
        """
        Calls the increment_page function with a value of -1. This will
        subtract one to the current page and then display that page.
        """
        guifunc.increment_page(self.parent, -1)

    def button_checked(self):
        """
        When the anti alias checkbox is checked/unchecked this code will re-render
        the currently displayed image with/without anti aliasing.
        """
        config.anti_alias = not config.anti_alias
        print(config.anti_alias)
        guifunc.resize_image(self.parent.image_display, toggled=True)


class ImageDisplay(tk.Label):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent: ImageViewer = parent

        self.config(background="black")
        self.bind("<Configure>", self.window_resized)
        self.bind("<Button-1>", self.hide_interface)

        self.initialise_image()

    def hide_interface(self, event) -> None:
        """
        Hides the top and bottom bar on the image viewer, making the image able to
        stretch from the very top of the window to the very bottom.
        """
        print(event)
        guifunc.hide_interface(self.parent)

    def window_resized(self, event) -> None:
        """
        When the label displaying the image is resized, scale the image to fit.
        """
        guifunc.window_resized(self, event)

    def initialise_image(self) -> None:
        """
        Display the initial image from the comic when the image viewer is opened.
        """
        root = self.parent
        guifunc.set_image(self, root.image_list[root.current_page])


class BottomDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent: ImageViewer = parent
        self.page_display = tk.Label(self)
        self.update_display(parent.current_page, parent.max_page)

        self.page_display.pack()

    def update_display(self, page=0, max_page=0):
        self.page_display.config(text=f"Page {page + 1}/{max_page + 1}")


class ImageViewer(tk.Tk):
    def __init__(self, path):
        super().__init__()

        self.path = path
        self.image_list = guifunc.extract_images_from_archive(self.path)
        self.current_image = None
        self.current_image_copy = None
        self.interface_hidden = False
        try:
            self.max_page = len(self.image_list) - 1
        except TypeError:
            self.max_page = 0
        self._current_page = 0
        self.drag_id = None

        self.toolbar = Toolbar(self)
        self.image_display = ImageDisplay(self)
        self.bottom_display = BottomDisplay(self)
        self.initialise_ui()

        self.bind("<Left>", self.toolbar.decrement_page)
        self.bind("<Right>", self.toolbar.increment_page)

    @property
    def current_page(self):
        return self._current_page

    @current_page.setter
    def current_page(self, var):
        print("setting current_page")

        if var < 0:
            var = 0
        elif var > self.max_page:
            var = self.max_page

        self._current_page = var
        self.bottom_display.update_display(self.current_page, self.max_page)

    # def resize_image(self, event) -> None:
    #     """
    #     Resizes the current image to fit the viewer while respecting window size and aspect ratio.
    #     """
    #     guifunc.resize_image(self.image_display, event)

    def initialise_ui(self):
        self.title("ComicReader")
        self.geometry("500x700")
        self.minsize(245, 350)

        # GRID GUI
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.toolbar.grid(row=0)
        self.image_display.grid(row=1, column=0, sticky="nsew")
        self.bottom_display.grid(row=2, column=0, sticky="ew")


def show_vars(obj) -> None:
    """
    Prints out all the variables from the passed object's dictionary.
    """
    for k, v in obj.__dict__.items():
        print(k, v)
