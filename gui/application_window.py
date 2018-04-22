import sys

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow

from color.color_spaces import RGB_BACKGROUND
from grid.grid_instance import grid
from gui.canvas import DragAndDropCanvas
from image.to_qimage import to_qimage


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._palette_size = grid.radius * 2
        self.setFixedWidth(self._palette_size)
        self.setFixedHeight(self._palette_size)

    def paintEvent(self, e):
        painter = QPainter(self)

        background = RGB_BACKGROUND
        qimage = to_qimage(background)
        painter.drawImage(QRect(0, 0, self._palette_size, self._palette_size), qimage)


def start():
    application = QApplication(sys.argv)
    main_window = ApplicationWindow()
    main_window.setCentralWidget(DragAndDropCanvas())
    main_window.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    start()
