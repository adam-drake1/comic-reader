from __future__ import annotations
from PIL import ImageTk
from typing import TYPE_CHECKING, List
import math
from debugging import debug
import io
import tkinter
from config import config
import zipfile
from PIL import Image

if TYPE_CHECKING:
    from image_viewer import ImageViewer, ImageDisplay

# TODO: MAKE IT SO WHEN THE IMAGE IS RESIZED THROUGH HIDING THE INTERFACE THAT IT IS AUTOMATICALLY ANTI ALIASED.


def extract_images_from_archive(path: str) -> List[io.BytesIO]:
    """
    Reads through every file in a zip archive and returns all .jpg files as a list of io.BytesIO objects.
    """
    with zipfile.ZipFile(path, "r") as my_zip:
        return [Image.open(io.BytesIO(my_zip.read(x))) for x in my_zip.filelist if ".jpg" in str(x)]


def set_image(obj: ImageDisplay, picture: io.BytesIO = None) -> None:
    """
    Updates the image that is shown in the image viewer
    :param obj: the object that shows the image
    :param picture: Pass an io.BytesIO image to forcibly change the current image. (e.g. on startup)
    """

    root = obj.parent

    if picture:
        root.current_image = picture
        root.current_image_copy = picture

    new_image = ImageTk.PhotoImage(root.current_image)
    obj.config(image=new_image)
    obj.image = new_image


def increment_page(obj: ImageViewer, change: int) -> None:

    old_page_number = obj.current_page
    obj.current_page += change

    current_page = obj.current_page

    if current_page is not old_page_number or change == 0:
        print("Updating Pages")
        obj.current_image = obj.image_list[current_page]
        obj.current_image_copy = obj.current_image

        resize_image(obj.image_display)
        obj.update()
    else:
        print("Page has not changed")


def hide_interface(self: ImageViewer):
    interface_hidden = self.interface_hidden

    if interface_hidden:
        self.toolbar.grid(row=0)
        self.bottom_display.grid(row=2, sticky="ew")
    else:
        self.toolbar.grid_forget()
        self.bottom_display.grid_forget()

    self.interface_hidden = not interface_hidden


def window_resized(obj: ImageDisplay, event: tkinter.Event) -> None:
    """
    Adds a delay between when the image is resized to fit the window and when anti aliasing is applied.
    This makes for much smoother window resizing.

    :param obj: the image viewer
    :param event: a tkinter event that is called whenever the image viewer is resized.
    """

    root = obj.parent

    def stop_dragging() -> None:
        # Now that the window hasn't been resized in x amount of time,
        # re-render the image with anti aliasing enabled.
        print("Resize stopped.")
        root.drag_id = None
        resize_image(obj, toggled=True)

    if config.anti_alias:
        if root.drag_id:
            # If window is already being dragged (already has a drag_id) then cancel the last after() call.
            root.after_cancel(root.drag_id)

        resize_image(obj, event, antialias=False)
        root.drag_id = root.after(25, stop_dragging)
    else:
        resize_image(obj, event)


@debug
def resize_image(obj: ImageDisplay, event=None, toggled: bool = False, debugging: bool = False, antialias: bool = None):
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

    root = obj.parent

    if antialias is None:
        antialias = config.anti_alias

    if debugging:
        print()
        print(f"Entering resize_image, antialias = {antialias}")

    def scale() -> (int, int):
        size = root.current_image_copy.size
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
        new_width, new_height = obj.winfo_width(), obj.winfo_height()

    old_size = root.current_image.size
    new_size = old_size if toggled else scale()
    size_change = (old_size != new_size)

    if debugging:
        print(f"Old size: {old_size}, New size: {new_size}")

    if size_change or toggled:
        root.current_image = root.current_image_copy.resize(new_size, antialias)
        set_image(root.image_display)
