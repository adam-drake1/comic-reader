import subprocess
import sys
import os
import PySide2
from zipfile import ZipFile
import config
from flow_layout import FlowLayout
from pathlib import Path

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QSize, QPoint
from PySide2.QtWidgets import QWidget, QPushButton, QToolTip, QApplication, QMessageBox, QMainWindow, QAction, QMenu, \
    QLabel, QSizePolicy, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QScrollArea
from PySide2.QtGui import QIcon, QFont, QKeySequence, Qt, QPixmap, QPalette, QColor, QImage

settings = config.Settings()

ZIP_TYPES = settings.zip_types
IMAGE_TYPES = settings.image_types
DIRECTORIES = settings.directories

# TODO: Use zoom value to change size of comics in explorer
# TODO: Allow filter panel to be resized with mouse


class Comic(QLabel):
    scaleX = 145
    scaleY = 200

    spaceX = 5

    def __init__(self, path: str, image: QPixmap, parent=None):
        super(Comic, self).__init__(parent)
        self.path = path
        self.image = image
        self.thumbnail = None

        # set_colour(self, Qt.yellow)
        self.set_image()

    def set_image(self):
        landscape = (self.image.size().width() > self.image.size().height())

        if landscape:
            self.scaleX = (self.scaleX * 2) + self.spaceX

        self.thumbnail = self.image.scaled(self.scaleX, self.scaleY, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(self.thumbnail)
        self.setFixedSize(self.scaleX, self.scaleY)
        self.setAlignment(Qt.AlignCenter)

    def contextMenuEvent(self, ev: PySide2.QtGui.QContextMenuEvent) -> None:
        """
        Handles the context menu that appears when you right click on a comic and their actions.

        :param ev: Event parameter used by PySide2, stores all the information about the right click event.
        """
        cmenu = QMenu()
        open_menu = QMenu("Open")

        open_menu.addAction("Open in HentaiReader")
        open_menu.addAction("Open in New Tab")
        open_menu.addAction("Open in Explorer", self.open_in_explorer)

        cmenu.addMenu(open_menu)
        cmenu.addAction("Info", lambda: print(self.path))
        cmenu.exec_(self.mapToGlobal(ev.pos()))

    def open_in_explorer(self):
        """
        Opens the targeted comic's location in file explorer / finder.
        :return:
        """
        if sys.platform == "win32":
            subprocess.Popen(f"explorer /select, {self.path}")
        else:
            print("OS not supported yet")


class ComicExplorer(QWidget):
    def __init__(self, parent, colour: QColor = None):
        super(ComicExplorer, self).__init__(parent)

        self.colour = colour
        self.layout = FlowLayout(self)

        if self.colour:
            set_colour(self, self.colour)

        self.init_ui()

    def init_ui(self):
        set_colour(self, self.colour)
        self.display_comics()

    def display_comics(self):

        def rename(directory):
            print(f"Searching {directory}")
            for file in os.listdir(directory):
                file_type = suffix(file)
                comic_path = os.path.join(directory, file)

                # If file is folder then search folder
                if file_type == "":
                    rename(comic_path)
                    continue

                # If file is a supported file type and contains an image then create Comic object.
                if file_type in ZIP_TYPES:
                    image = _image_from_zip(comic_path)

                    if image:
                        self.layout.addWidget(Comic(comic_path, image, self))

        for x in DIRECTORIES:
            rename(x)


def _image_from_zip(path: str) -> QPixmap:
    """
    Open an archive file at path and return a QPixmap containing the first image found in the archive.
    If no supported images found, returns None.

    :param path: Path to the comic book archive including file name and extension.
    :return: QPixmap
    """

    with ZipFile(path, "r") as my_zip:
        for x in my_zip.filelist:
            if suffix(x.filename) in IMAGE_TYPES:
                image = my_zip.read(x)
                qp = QPixmap()
                qp.loadFromData(image)
                image = qp
                return image


def suffix(path):
    return Path(path).suffix


class MainWindow(QMainWindow):
    def __init__(self, debug=False):
        super(MainWindow, self).__init__()

        self.debug = debug
        self.layout = QHBoxLayout()

        self.init_ui()

    def init_ui(self):
        self.resize(1000, 900)
        self.setWindowTitle("HentaiReader")
        icon = QIcon(QPixmap("images/count.png"))
        self.setWindowIcon(icon)

        self.setCentralWidget(make_widget(self, Qt.red, debug=self.debug))
        self.centralWidget().setLayout(self.layout)

        filter_panel = make_widget(self, Qt.blue, debug=self.debug)
        filter_panel.setFixedWidth(250)
        self.layout.addWidget(filter_panel)

        comic_explorer = ComicExplorer(self, Qt.green)
        self.layout.setMargin(3)
        self.layout.setSpacing(5)

        scroll_area = QScrollArea(self)
        scroll_area.setWidget(comic_explorer)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)


def set_colour(obj, colour):
    bg = QPalette()
    bg.setColor(QPalette.Window, colour)
    obj.setPalette(bg)
    obj.setAutoFillBackground(True)


def make_widget(parent, colour: QColor = None, *, max_height: int = None, debug: bool = None) -> QWidget:
    widget = QWidget(parent)

    if max_height is not None:
        widget.setMaximumHeight(max_height)

    if colour and debug:
        set_colour(widget, colour)
    return widget


def make_layout(parent=None, layout=None, *, margin: int = None, spacing: int = None):
    layout = layout()

    if margin is not None:
        layout.setMargin(margin)

    if spacing is not None:
        layout.setSpacing(spacing)

    parent.setLayout(layout)
    return layout


def main():
    app = QtWidgets.QApplication([])
    root = MainWindow(debug=True)
    root.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
