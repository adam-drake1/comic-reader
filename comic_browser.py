import sys
import os
import PySide2
from zipfile import ZipFile
import config

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QWidget, QPushButton, QToolTip, QApplication, QMessageBox, QMainWindow, QAction, QMenu, \
    QLabel, QSizePolicy, QGridLayout, QHBoxLayout
from PySide2.QtGui import QIcon, QFont, QKeySequence, Qt, QPixmap, QPalette, QColor, QImage

TEST_DIRECTORY = r"D:\Porn\Hentai\test"
settings = config.Settings()


class Comic(QLabel):
    image_types = ["jpg", "png"]
    zip_types = ["cbz", "zip"]

    def __init__(self, path=None, parent=None):
        super(Comic, self).__init__(parent)

        self.path = path.lower()
        self.parent = parent
        self.filename, self.file_type = self.path.split(".")

        image_file = (self.file_type in self.image_types)
        zip_file = (self.file_type in self.zip_types)

        print(f"testing {self.path}")
        if zip_file:
            self.image = self._image_from_zip(path)
        elif image_file:
            pass
        else:
            raise ValueError(self.file_type)

        print(f"Displaying {self.path}")

        self.thumbnail = self.image.scaled(parent.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setPixmap(self.image)

        print("finished")

    def _image_from_zip(self, path):
        with ZipFile(path, "r") as my_zip:
            for x in my_zip.filelist:
                if x.filename.split(".")[-1] in self.image_types:
                    image = my_zip.read(x)
                    qp = QPixmap()
                    qp.loadFromData(image)
                    image = qp
                    print("Image found")
                    break
        return image if image else QPixmap()

    def resizeEvent(self, event: PySide2.QtGui.QResizeEvent):
        self.thumbnail = self.image.scaled(self.parent.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(self.thumbnail)


class ComicWidget(QWidget):
    def __init__(self, parent, colour: QColor = None):
        super(ComicWidget, self).__init__(parent)

        self.colour = colour
        self.layout = QGridLayout()
        self.displayed_comics = {}

        if self.colour:
            self.colour_widget()

        self.init_ui()

    def colour_widget(self):
        bg = QPalette()
        bg.setColor(QPalette.Window, self.colour)

        self.setPalette(bg)
        self.setAutoFillBackground(True)

    def init_ui(self):
        self.setLayout(self.layout)

        zip_types = ["cbz", "zip"]
        count = 0
        for directory in settings.directories:
            for file in os.listdir(directory):
                comic_path = os.path.join(TEST_DIRECTORY, file)
                file_type = file.split(".")[-1]

                if file_type in zip_types:
                   comic = Comic(comic_path, self)

                if comic:
                    self.layout.addWidget(comic, 0, count)
                    count += 1


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.layout = QGridLayout()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.centralWidget().setLayout(self.layout)

        bg = QPalette()
        bg.setColor(QPalette.Window, Qt.red)
        self.central_widget.setPalette(bg)
        self.central_widget.setAutoFillBackground(True)

        self.comic_widget = ComicWidget(self, Qt.green)
        self.layout.addWidget(self.comic_widget)

        self.init_ui()

    def init_ui(self):
        self.resize(500, 300)
        self.setWindowTitle("HentaiReader")
        icon = QIcon(QPixmap("images/count.png"))
        self.setWindowIcon(icon)


def main():
    app = QtWidgets.QApplication([])
    root = MainWindow()
    root.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
