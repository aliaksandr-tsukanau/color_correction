import sys

from PyQt5.QtCore import QRect, Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow

from color.correction import AB_UNIQUE_FOR_PYQT
from color.palette import RGB_BACKGROUND
from grid.grid_instance import grid
from gui.canvas import DragAndDropCanvas
from image.to_qimage import to_qimage
from image.image import INITIAL_IMAGE


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._palette_size = grid.radius * 2
        self.setFixedWidth(self._palette_size +\
                           INITIAL_IMAGE.shape[1] * self._palette_size / INITIAL_IMAGE.shape[0])
                           # to exactly fit the picture
        self.setFixedHeight(self._palette_size)

    def paintEvent(self, e):
        painter = QPainter(self)

        background = to_qimage(RGB_BACKGROUND)
        painter.drawImage(QRect(0, 0, self._palette_size, self._palette_size), background)

        initial_image = to_qimage(INITIAL_IMAGE)
        scaled_img = initial_image.scaledToHeight(self._palette_size, Qt.SmoothTransformation)
        painter.drawImage(QPoint(self._palette_size, 0), scaled_img)

        self._draw_present_colors(painter)
        self._draw_invisible_nodes(painter)

    def _draw_present_colors(self, painter: QPainter):
        """Mark colors present in initial picture as white dots on palette"""
        painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
        for ab in AB_UNIQUE_FOR_PYQT:
            painter.drawPoint(ab[1], ab[0])
            # 1, then 0 is no mistake

    def _draw_invisible_nodes(self, painter: QPainter):
        painter.setPen(QPen(Qt.darkYellow, 1, Qt.SolidLine))
        for branch in grid.invisible_nodes:
            for ab in branch:
                painter.drawPoint(*(ab + grid.radius))


def start():
    application = QApplication(sys.argv)
    main_window = ApplicationWindow()
    main_window.setCentralWidget(DragAndDropCanvas())
    main_window.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    start()
