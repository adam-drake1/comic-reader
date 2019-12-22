from pathlib import Path
from zipfile import ZipFile
from PySide2.QtGui import QPixmap

from comic_browser import IMAGE_TYPES


def image_from_path_to_zip(path: str) -> QPixmap:
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
