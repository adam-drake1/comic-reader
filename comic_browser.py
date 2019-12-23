import copy
import subprocess
import sys
import os
import PySide2

from config import settings
from flow_layout import FlowLayout
import gui_functions
from my_widgets import make_widget, DefaultWidget, ZoomSlider

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QWidget, QApplication, QMainWindow, QAction, QMenu, \
    QLabel, QHBoxLayout, QScrollArea, QVBoxLayout, QSlider, QAbstractSlider, QSplitter, QDialog
from PySide2.QtGui import QIcon, Qt, QPixmap, QPalette, QColor

ZIP_TYPES = settings.zip_types
IMAGE_TYPES = settings.image_types
DIRECTORIES = settings.directories

# TODO: Add Qsplitter to filter panel


class Comic(QLabel):
    # TODO: Need to add some kind of metadata to comic files and store said metadata
    # TODO: Use zoom value to change size of comics in explorer
    comicHeight = 200
    comicWidth = comicHeight * 0.7
    # comicWidth = 145

    comicSpacer = 5

    def __init__(self, path: str, image: QPixmap, parent=None):
        super(Comic, self).__init__(parent)
        self.path = path
        self.image = image
        self.thumbnail = None
        self.landscape = (self.image.size().width() > self.image.size().height())

        settings.explorerZoom.bind_to(self.test_zoom)
        self.set_image()

    def test_zoom(self, value):
        scaled_width = self.comicWidth * value
        scaled_height = self.comicHeight * value

        if self.landscape:
            scaled_width = (scaled_width * 2) + self.comicSpacer

        self.thumbnail = self.image.scaled(scaled_width, scaled_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(self.thumbnail)
        self.setFixedSize(scaled_width, scaled_height)

    def set_image(self):
        scaled_width = self.comicWidth * settings.explorerZoom.get_zoom()
        scaled_height = self.comicHeight * settings.explorerZoom.get_zoom()

        if self.landscape:
            scaled_width = (scaled_width * 2) + self.comicSpacer

        self.thumbnail = self.image.scaled(scaled_width, scaled_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(self.thumbnail)
        self.setFixedSize(scaled_width, scaled_height)
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


class ComicExplorer(DefaultWidget):
    def __init__(self):
        super(ComicExplorer, self).__init__(debug_colour=Qt.green)

        self.defaultColour = QApplication.style().standardPalette()
        self.layout = FlowLayout(self)

        self.display_comics()

    def display_comics(self):
        def rename(directory):
            print(f"Searching {directory}")
            for file in os.listdir(directory):
                file_type = gui_functions.suffix(file)
                comic_path = os.path.join(directory, file)

                # If file is folder then search folder
                if file_type == "":
                    rename(comic_path)
                    continue

                # If file is a supported file type and contains an image then create Comic object.
                if file_type in ZIP_TYPES:
                    image = gui_functions.image_from_path_to_zip(comic_path)

                    if image:
                        self.layout.addWidget(Comic(comic_path, image, self))

        for x in DIRECTORIES:
            rename(x)


class InfoBar(DefaultWidget):
    """
    Displays information to the user and allows users to adjust how large comics are in the comic explorer (zoom)
    """
    def __init__(self):
        super(InfoBar, self).__init__(debug_colour=Qt.cyan)
        self.zoom_slider = ZoomSlider(Qt.Horizontal, self)

    def init_ui(self):
        pass


class SettingsWindow(DefaultWidget):
    def __init__(self):
        super(SettingsWindow, self).__init__(debug_colour=Qt.cyan)

        self.defaultColour = QApplication.style().standardPalette()

        self.debug = QtWidgets.QCheckBox("Enable/Disable debug mode?", self)
        self.debug.setChecked(bool(settings.debug))
        self.debug.clicked.connect(self.debug_clicked)

    def debug_clicked(self):
        settings.debug.set_debug(self.debug.isChecked())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.create_actions()
        self.create_menus()

        self.verticalOuterLayout = QVBoxLayout()
        self.horizontalInnerLayout = QHBoxLayout()
        self.settingsWindow = SettingsWindow()
        self.infoBar = InfoBar()
        self.splitter = Splitter(self, 250, "fill")

        self.init_main_window_ui()
        settings.debug.set_debug(True)

    def init_main_window_ui(self):
        self.resize(1000, 900)
        self.setWindowTitle("HentaiReader")
        icon = QIcon(QPixmap("images/count.png"))
        self.setWindowIcon(icon)

        # setting up the central widget and main layouts for our widgets.
        self.setCentralWidget(make_widget(self))
        self.centralWidget().setLayout(self.verticalOuterLayout)
        horizontal_inner_layout_widget = make_widget(self, Qt.red)
        horizontal_inner_layout_widget.setLayout(self.horizontalInnerLayout)
        self.verticalOuterLayout.setMargin(0)
        self.verticalOuterLayout.setSpacing(0)
        self.horizontalInnerLayout.setMargin(3)
        self.verticalOuterLayout.addWidget(horizontal_inner_layout_widget)

        # filter panel is the left-most panel that stores users' filtered comic list.
        filter_panel = make_widget(self, Qt.blue)

        # comic explorer is where the comics are displayed.
        comic_explorer = ComicExplorer()

        # scroll area houses the comic explorer, so that you can scroll through comics if there
        # are too many to display on a single monitor.
        scroll_area = QScrollArea(self)
        scroll_area.setWidget(comic_explorer)
        scroll_area.setWidgetResizable(True)

        self.horizontalInnerLayout.addWidget(self.splitter)
        self.splitter.addWidget(filter_panel)
        self.splitter.addWidget(scroll_area)

        # info bar is the thin bar at the bottom of the window.
        self.infoBar.setFixedHeight(30)
        self.verticalOuterLayout.addWidget(self.infoBar)

    def create_actions(self):
        self.settingsAction = QAction("Settings", self, triggered=self.settings_window)

    def create_menus(self):
        self.fileMenu = self.menuBar().addMenu("File")
        self.fileMenu.addAction(self.settingsAction)

    def settings_window(self):
        # TODO: Make it so that the settings window closes when the main window closes
        self.settingsWindow.show()


class Splitter(QSplitter):
    def __init__(self, parent, *args):
        super().__init__(parent)
        self.widget_sizes = [*args]

        self.resizeEvent = self.resize_decorator(self.resizeEvent)
        self.splitterMoved.connect(self.splitter_moved)

    def splitter_moved(self, pos, index):
        self.widget_sizes[index - 1] = pos

    def resize_decorator(self, func):
        def wrapper(*args):
            func(*args)
            sizes = []
            for size in self.widget_sizes:
                if isinstance(size, int):
                    sizes.append(size)
                elif size == "fill":
                    sizes.append(self.size().width() - sum(sizes) - (self.handleWidth() * len(sizes)))
                    break
            self.setSizes(sizes)
        return wrapper


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    root = MainWindow()
    root.show()
    sys.exit(app.exec_())
