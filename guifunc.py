from __future__ import annotations
from PIL import ImageTk
from typing import TYPE_CHECKING
import math
from debugging import debug
import io
import tkinter

if TYPE_CHECKING:
    from app_interface import ImageViewer

# TODO: MAKE IT SO WHEN THE IMAGE IS RESIZED THROUGH HIDING THE INTERFACE THAT IT IS AUTOMATICALLY ANTIALIASED.


def set_image(self: ImageViewer, picture: io.BytesIO = None) -> None:
    """
    Updates the image that is shown in the image viewer
    :param self: the object that shows the image
    :param picture: Pass an io.BytesIO image to forcibly change the current image. (e.g. on startup)
    """

    if picture:
        self.settings.current_image = picture
        self.settings.current_image_copy = picture

    new_image = ImageTk.PhotoImage(self.settings.current_image)
    self.image_display.config(image=new_image)
    self.image_display.image = new_image


def update_page_display(self: ImageViewer) -> None:
    """
    Updates the page counter at the bottom of the image viewer
    """

    current_page = self.settings.current_page + 1
    max_page = self.settings.max_pages + 1
    self.page_display.config(text=f"Page {current_page}/{max_page}")


def increment_page(self: ImageViewer, change):
    old_page_number = self.settings.current_page
    current_page = old_page_number + change
    max_page = self.settings.max_pages

    if current_page < 0:
        current_page = 0
    elif current_page > max_page:
        current_page = max_page

    if old_page_number is not current_page or change == 0:
        print("Updating Pages")
        self.settings.current_page = current_page
        self.settings.current_image = self.settings.list_of_images[self.settings.current_page]
        self.settings.current_image_copy = self.settings.current_image

        update_page_display(self)
        resize_image(self)
        self.parent.update()
    else:
        print("Page has not changed")


def hide_interface(self: ImageViewer):
    interface_hidden = self.settings.interface_hidden

    if interface_hidden:
        self.topFrame.grid(row=0, sticky="ew")
        self.bottomFrame.grid(row=2, sticky="ew")
    else:
        self.topFrame.grid_forget()
        self.bottomFrame.grid_forget()

    self.settings.interface_hidden = not interface_hidden


def window_resized(self: ImageViewer, event: tkinter.Event) -> None:
    """
    Adds a delay between when the image is resized to fit the window and when antialiasing is applied.
    This makes for much smoother window resizing.

    :param self: the image viewer
    :param event: a tkinter event that is called whenever the image viewer is resized.
    """

    def stop_dragging() -> None:
        self.settings.drag_id = None
        resize_image(self, toggled=True)

    if self.settings.ANTIALIAS.get() is True:
        if self.settings.drag_id:
            # If window is already being dragged (already has a drag_id) then cancel the last after() call.
            self.parent.after_cancel(self.settings.drag_id)

        resize_image(self, event, antialias=False, debugging=False)
        self.settings.drag_id = self.parent.after(25, stop_dragging)
    else:
        resize_image(self, event)


@debug
def resize_image(self: ImageViewer, event=None, toggled: bool = False, debugging: bool = False, antialias: bool = None):
    """
    Resizes the original image to fit the frame if the size has changed.
    Called when image is changed or from the window_resized function.

    :param self: the instance of the image viewer.
    :param toggled: True when the antialias button is checked. Does not change the size of the image.
    :param debugging: Display extra output if true.
    :param antialias: Set to true if you would like the image to be aliased. If nothing is passed
                      then the value from the application's settings will be used.

    :type event: Called whenever the image viewing window changes size.
    """

    if antialias is None:
        antialias = self.settings.ANTIALIAS.get()

    if debugging:
        print()
        print(f"Entering {resize_image.__name__}, antialias = {antialias}")

    def scale() -> (int, int):
        size = self.settings.current_image_copy.size
        asp_ratio = min(size)/max(size)

        if debugging:
            print("Image size: {0}x{1}".format(*size))
            print(f"Aspect ratio: {asp_ratio}")

        x, y = size
        fx, fy = new_width, new_height
        landscape = (x > y)

        # check if image is portrait or landscape and scale to fit frame
        x, y = fx if landscape else math.ceil(fy * asp_ratio), math.ceil(fx * asp_ratio) if landscape else fy

        # if x or y is bigger than the frame, resize them by their aspect ratio
        if x > fx:
            x, y = fx, math.ceil(fx / asp_ratio)
        elif y > fy:
            y, x = fy, math.ceil(fy / asp_ratio)
        return x, y

    if event:
        new_width = event.width
        new_height = event.height
    else:
        new_width, new_height = self.image_display.winfo_width(), self.image_display.winfo_height()

    old_size = self.settings.current_image.size
    new_size = old_size if toggled else scale()
    size_change = (old_size != new_size)

    if debugging:
        print(f"Old size: {old_size}, New size: {new_size}")

    if size_change or toggled:
        self.settings.current_image = self.settings.current_image_copy.resize(new_size, antialias)
        set_image(self)
