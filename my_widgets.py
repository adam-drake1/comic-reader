from PySide2.QtGui import QColor, Qt, QPalette
from PySide2.QtWidgets import QWidget, QApplication, QSlider

from config import settings


class ZoomSlider(QSlider):
    def __init__(self, *args):
        super().__init__(*args)

        self.setMinimum(settings.explorerZoom.zoomScale * 0.5)
        self.setMaximum(settings.explorerZoom.zoomScale * 3)
        self.setValue(settings.explorerZoom.get_zoom() * settings.explorerZoom.zoomScale)
        self.valueChanged.connect(self.change_zoom)
        self.setPageStep(1)

    def change_zoom(self, value):
        settings.explorerZoom.set_zoom(self.value())


def make_widget(*args, **kwargs):
    return DefaultWidget(*args, **kwargs)


class ObserverWidget(QWidget):
    def __init__(self):
        super().__init__()
        settings.debug.bind_to(self.debug_mode)     # bind to settings.debug variable with observer pattern

        self.debugColour = None
        self.defaultColour = None

    def debug_mode(self, debugging=False):
        recolour_for_debugging = (debugging and self.debugColour)

        if recolour_for_debugging:
            self.set_widget_colour(self.debugColour)
        else:
            self.set_widget_colour(self.defaultColour)

    def set_widget_colour(self, colour=None):
        """
        Changes the colour of the widget.

        colour: Accepts either Qt.GlobalColour (Qt.red) or QPalette input anything else will do nothing.
        """
        if colour:
            if isinstance(colour, Qt.GlobalColor):
                bg = QPalette()
                bg.setColor(QPalette.Window, colour)
            elif isinstance(colour, QPalette):
                bg = colour
            else:
                return

            self.setPalette(bg)
            self.setAutoFillBackground(True)


class DefaultWidget(ObserverWidget):
    def __init__(self, parent=None, debug_colour: QColor = None, *, max_height: int = None):
        super().__init__()

        if parent:
            self.parent = parent
        self.defaultColour = QApplication.style().standardPalette()
        self.debugColour = debug_colour

        if max_height is not None:
            self.widget.setMaximumHeight(max_height)
