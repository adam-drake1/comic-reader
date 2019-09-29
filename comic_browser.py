import sys
from PySide2 import QtWidgets, QtGui
from PySide2.QtWidgets import QWidget, QPushButton, QToolTip, QApplication, QMessageBox, QMainWindow, QAction, QMenu
from PySide2.QtGui import QIcon, QFont, QKeySequence, Qt


class Comic(QWidget):
    def __init__(self, path=None):
        super().__init__()

        self.path = path
        

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.init_ui()
        
    def init_ui(self):
        self.setToolTip("This is a widget")

        self.setGeometry(300, 300, 245, 350)
        self.setWindowTitle("HentaiReader")
        self.setWindowIcon(QIcon("images/count.png"))

        self.show()
        self.center()

    def center(self):
        qr = self.frameGeometry()
        screen = self.windowHandle().screen()
        cp = screen.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        mbox = QMessageBox()
        mbox.setWindowTitle("Critical alert from Microsoft")
        mbox.setText("Due to security notification we find that your microsoft windows has crashed down")
        mbox.setInformativeText("Do you still want to quit?")
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        mbox.setDefaultButton(QMessageBox.No)

        reply = mbox.exec_()

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        print("key pressed")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.statusbar = self.statusBar()

        self.init_ui()

    def init_ui(self):
        self.statusbar.showMessage("Ready")

        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        edit_menu = menu.addMenu("Edit")
        view_menu = menu.addMenu("View")

        exit_act = QAction(text="Exit", parent=self)
        exit_act.setShortcut(QKeySequence("Ctrl+Q"))
        exit_act.setStatusTip("Exit application")
        exit_act.triggered.connect(QApplication.instance().quit)

        settings_act = QAction(text="Open Window", parent=self)
        settings_act.setStatusTip("Open Settings Window")
        settings_act.triggered.connect(lambda: print("settings clicked"))

        view_stat_act = QAction(text="View Statusbar", parent=self)
        view_stat_act.setStatusTip("View Statusbar")
        view_stat_act.setCheckable(True)
        view_stat_act.setChecked(True)
        view_stat_act.triggered.connect(self.toggle_menu)

        settings_menu = QMenu("Preferences")
        settings_menu.addAction(settings_act)

        file_menu.addAction(exit_act)

        edit_menu.addMenu(settings_menu)

        view_menu.addAction(view_stat_act)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Main Window")
        self.show()

    def toggle_menu(self, state):
        print(state)
        if state:
            self.statusbar.show()
            self.statusbar.showMessage("Ready")
        else:
            self.statusbar.hide()


if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    root = MainWindow()

    pix = QtGui.QPixmap("images/comic1.jpg")

    sys.exit(app.exec_())
