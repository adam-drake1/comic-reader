from image_viewer import ImageViewer, show_vars
from config import config


if __name__ == "__main__":

    # comic = r"C:\Users\adrake.KEMPTOWN\Pictures\onepunchman\onepunchman.cbz"
    # comic = r"D:\Downloads\gallery.zip"

    my_gui = ImageViewer(comic)
    show_vars(config)
    show_vars(ImageViewer)

    my_gui.mainloop()
