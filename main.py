import zipfile
import os
from PIL import Image
import io
import tkinter as tk
from app_interface import ImageViewer, show_vars

directory = r"D:\Porn\Hentai\Doujinshi\Circle-FIORE\Oneshot"
comic = "I want to Share my Love through my Mouth SAGA (2019).cbz"
# comic = "Oneshot.zip"

os.chdir(directory)


def extract_images_from_archive(path):
    with zipfile.ZipFile(path, "r") as myzip:
        return [Image.open(io.BytesIO(myzip.read(x))) for x in myzip.filelist if ".jpg" in str(x)]


if __name__ == "__main__":

    list_of_files = extract_images_from_archive(comic)

    root = tk.Tk()
    root.geometry("500x700")
    my_gui = ImageViewer(root, list_of_files)
    show_vars(my_gui.settings)

    root.mainloop()
