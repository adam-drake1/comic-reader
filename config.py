import tkinter as tk
import os
import zipfile
from PIL import Image
import io

directory = r"C:\Users\adrake.KEMPTOWN\Pictures\onepunchman"
comic = "onepunchman.cbz"
os.chdir(directory)


def extract_images_from_archive(path):
    with zipfile.ZipFile(path, "r") as myzip:
        return [Image.open(io.BytesIO(myzip.read(x))) for x in myzip.filelist if ".jpg" in str(x)]


class Settings:
    def __init__(self, list_of_images=None):
        self.list_of_images = extract_images_from_archive(comic)
        self.current_image = None
        self.current_image_copy = None
        self.current_page = 0
        # self.anti_alias = tk.BooleanVar()
        self.anti_alias = False
        self.interface_hidden = False
        self.drag_id = None

    @property
    def max_pages(self):
        try:
            return len(self.list_of_images) - 1
        except TypeError:
            return 0




config = Settings()
