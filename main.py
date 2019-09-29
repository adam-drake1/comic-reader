from image_viewer import ImageViewer, show_vars
from config import config

if __name__ == "__main__":

    # comic = r"C:\Users\adrake.KEMPTOWN\Pictures\onepunchman\onepunchman.cbz"
    # comic = r"D:\Downloads\gallery.zip"
    comic = "D:\Porn\Hentai\Doujinshi\Tamarun\Andria La Land\Andira La La Land II (2018).cbz"

    my_gui = ImageViewer(comic)
    show_vars(config)
    show_vars(ImageViewer)

    my_gui.mainloop()
