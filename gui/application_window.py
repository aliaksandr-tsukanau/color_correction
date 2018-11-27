import sys
from copy import deepcopy

from PyQt5.QtCore import QRect, Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction

from color.palette import Palette
from grid.grid import Grid
from image.image import get_unique_colors_for_pyqt
from gui.canvas import DragAndDropCanvas
from image.to_qimage import to_qimage
from image.image import read_initial_rgb, initial_to_lab, correct_image


class ApplicationWindow(QMainWindow):
    def __init__(self, grid, palette):
        super().__init__()
        self.aaa = 0
        self._palette = palette
        self._grid = grid
        self._palette_size = grid.radius * 2

        self.initial_rgb = read_initial_rgb()
        self.initial_lab = initial_to_lab(self.initial_rgb)
        self.processed = deepcopy(self.initial_rgb)

        self._set_up_ui()

        self.unique = get_unique_colors_for_pyqt(self.initial_rgb, grid.radius)

    def _set_up_ui(self):
        self.setFixedWidth(self._palette_size
                           + self.initial_rgb.shape[1] * self._palette_size / self.initial_rgb.shape[0])
        # to exactly fit the picture
        self.setFixedHeight(self._palette_size)

    def paintEvent(self, e):
        print(self.aaa)
        self.aaa+=1
        painter = QPainter(self)

        background = to_qimage(self._palette.rgb)
        painter.drawImage(QRect(0, 0, self._palette_size, self._palette_size), background)

        initial_image = to_qimage(self.processed)
        scaled_img = initial_image.scaledToHeight(self._palette_size, Qt.SmoothTransformation)
        painter.drawImage(QPoint(self._palette_size, 0), scaled_img)
        if self.aaa < 10:
            self._draw_present_colors(painter)
        # self._draw_invisible_nodes(painter)

    def _draw_present_colors(self, painter: QPainter):
        """Mark colors present in initial picture as white dots on palette"""
        painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
        for ab in self.unique:
            painter.drawPoint(*ab)

    def _draw_invisible_nodes(self, painter: QPainter):
        # for debugging
        painter.setPen(QPen(Qt.darkYellow, 2, Qt.SolidLine))
        for branch in self._grid.invisible_nodes:
            for ab in branch:
                painter.drawPoint(*(ab + self._grid.radius))


def start():
    application = QApplication(sys.argv)

    grid = Grid(branches_number=8, radius=250, invisible_branches=320, inv_nodes_per_branch=71)
    palette = Palette(grid)

    main_window = ApplicationWindow(grid, palette)
    main_window.setCentralWidget(DragAndDropCanvas(grid, palette, parent=main_window))
    main_window.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    start()
