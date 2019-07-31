import tkinter as tk
import guifunc

# TODO: LEFT AND RIGHT ARROWS ON KEYBOARD TO SWITCH BETWEEN IMAGES


class ImageViewer:
    def __init__(self, parent, list_of_images=None):
        self.parent = parent
        self.settings = self.Settings(list_of_images)
        parent.title("ComicReader")
        parent.minsize(210, 300)

        self.topFrame = tk.Frame(parent)
        self.bottomFrame = tk.Frame(parent)
        self.topMiddleFrame = tk.Frame(self.topFrame)

        self.prev_button = tk.Button(self.topMiddleFrame, text="<", command=self.decrement_page)
        self.next_button = tk.Button(self.topMiddleFrame, text=">", command=self.increment_page)
        self.aa_enable = tk.Checkbutton(self.topMiddleFrame)
        
        self.aa_enable.config(text="anti aliasing", variable=self.settings.ANTIALIAS, command=self.antialias_toggled)
        self.aa_enable.select()

        self.page_display = tk.Label(self.bottomFrame)
        self.page_display.config(text=f"Page {self.settings.current_page + 1}/{self.settings.max_pages + 1}")

        self.image_display = tk.Label(self.parent, background="black")
        self.image_display.bind("<Configure>", self.window_resized)
        self.image_display.bind("<Button-1>", self.hide_interface)

        # PACK GUI
        """
        You will need to change the parent of the topFrame buttons from self.topMiddleFrame to self.parent
        
        self.topFrame.pack()
        self.prev_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.LEFT)
        self.aa_enable.pack(side=tk.LEFT)
        self.bottomFrame.pack(side=tk.BOTTOM)
        self.page_display.pack(side=tk.LEFT)
        self.image_display.pack(fill=tk.BOTH, expand=tk.YES)
        """

        # GRID GUI
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=1)

        self.topFrame.grid(row=0, column=0, sticky="ew")
        self.topMiddleFrame.pack()
        self.image_display.grid(row=1, column=0, sticky="nsew")
        self.bottomFrame.grid(row=2, column=0, sticky="ew")

        self.prev_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.LEFT)
        self.aa_enable.pack(side=tk.LEFT)
        self.page_display.pack()

        self.initialise_image()

    def initialise_image(self) -> None:
        """
        Display the initial image from the comic when the image viewer is opened.
        """
        guifunc.set_image(self, self.settings.list_of_images[self.settings.current_page])

    def increment_page(self) -> None:
        """
        Calls the increment_page function with a value of 1. This will
        add one to the current page and then display that page.
        """
        guifunc.increment_page(self, 1)

    def decrement_page(self) -> None:
        """
        Calls the increment_page function with a value of -1. This will
        subtract one to the current page and then display that page.
        """
        guifunc.increment_page(self, -1)

    def antialias_toggled(self) -> None:
        """
        When the antialias checkbox is checked/unchecked this code will re-render
        the currently displayed image with/without antialiasing.
        """
        guifunc.resize_image(self, toggled=True)

    def window_resized(self, event) -> None:
        """
        When the label displaying the image is resized, scale the image to fit.
        """
        guifunc.window_resized(self, event)

    def resize_image(self, event) -> None:
        """
        Resizes the current image to fit the viewer while respecting window size and aspect ratio.
        """
        guifunc.resize_image(self, event)

    def hide_interface(self, event) -> None:
        """
        Hides the top and bottom bar on the image viewer, making the image able to
        stretch from the very top of the window to the very bottom.
        """
        print(event)
        guifunc.hide_interface(self)

    class Settings:
        def __init__(self, list_of_images=None):
            self.list_of_images = list_of_images
            self.current_image = None
            self.current_image_copy = None
            self.current_page = 0
            self.ANTIALIAS = tk.BooleanVar()
            self.interface_hidden = False
            self.drag_id = None
            try:
                self.max_pages = len(list_of_images) - 1
            except TypeError:
                self.max_pages = 0


def show_vars(obj) -> None:
    """
    Prints out all the variables from the passed object's dictionary.
    """
    for k, v in obj.__dict__.items():
        print(k, v)
