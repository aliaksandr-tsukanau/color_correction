#  Copyright (c) 2019 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#
#

import sys
from copy import deepcopy

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QShortcut, QInputDialog, QMenu
from skimage import transform
import numpy as np

from color.palette import Palette
from db.grid_driver import GridMongoClient
from grid.grid import Grid
from image.image import get_unique_colors_for_pyqt
from desktop.canvas import DragAndDropCanvas
from image.to_qimage import to_qimage
from image.image import read_initial_rgb, initial_to_lab


class ApplicationWindow(QMainWindow):
    def __init__(self,
                 grid: Grid,
                 palette: Palette,
                 db_client: GridMongoClient,
                 ):

        super().__init__()
        self._palette = palette
        self._grid = grid
        self._palette_size = grid.radius * 2

        self._db_client = db_client

        self.initial_rgb = read_initial_rgb()
        self.initial_lab = initial_to_lab(self.initial_rgb)
        self.processed = deepcopy(self.initial_rgb)

        self._set_up_ui()
        self._set_up_shortcuts()

        self.unique = get_unique_colors_for_pyqt(self.initial_rgb, grid.radius)
        # self._background = self._construct_palette_with_unique_colors_layer()

    def _set_up_ui(self):

        menubar = self.menuBar()

        img_menu = menubar.addMenu('Image')
        open_img = QAction('Open', self)
        save_img = QAction('Save', self)
        img_menu.addAction(open_img)
        img_menu.addAction(save_img)

        grid_menu = menubar.addMenu('Grid')
        download_grid = QAction('Download', self)
        download_grid.triggered.connect(self._load_grid)
        upload_grid = QAction('Upload', self)
        upload_grid.triggered.connect(self._write_grid)
        grid_menu.addAction(download_grid)
        grid_menu.addAction(upload_grid)

        self.setFixedWidth(self._palette_size
                           + self.initial_rgb.shape[1] * self._palette_size / self.initial_rgb.shape[0])
        # to exactly fit the picture
        # self.setFixedHeight(self._palette_size)

    def _set_up_shortcuts(self):
        handlers = {
            'Ctrl+O': self._open_image,
            'Ctrl+S': self._save_image,
            'Ctrl+L': self._load_grid,
            'Ctrl+W': self._write_grid,
        }
        self._shortcuts = {}
        for shortcut, handler in handlers.items():
            s = QShortcut(QKeySequence(shortcut), self)
            s.activated.connect(handler)
            self._shortcuts[shortcut] = s

    def _open_image(self):
        print('O')

    def _save_image(self):
        print('S')

    def _load_grid(self):
        name, ok = QInputDialog.getText(self, 'Ready to load', 'What filter do you want to load?')
        if not ok:
            return
        try:
            grid = self._db_client.get_grid_obj(name)
            self._grid = grid
            self.centralWidget()._grid = grid
            self.centralWidget().update()
            self.centralWidget().update_image()
        except TypeError:
            print('Not found')

    def _write_grid(self):
        name, ok = QInputDialog.getText(self, 'Ready to save', 'Choose a name for your filter:')
        if ok:
            self._db_client.save_grid(self._grid, name)\

    def paintEvent(self, e):
        painter = QPainter(self)
        #
        # painter.drawImage(QPoint(0, 0), self._background)

        # image = to_qimage(self.processed)
        # scaled_img = image.scaledToHeight(self._palette_size, Qt.SmoothTransformation)
        # painter.drawImage(QPoint(self._palette_size, 0), scaled_img)

        # self._draw_invisible_nodes(painter)

    def _construct_palette_with_unique_colors_layer(self):
        background = transform.resize(self._palette.rgb, (self._palette_size, self._palette_size))
        background = 255 * background
        for b, a in self.unique:
            background[int(a), int(b)] = 255
        background = np.require(background, np.uint8, 'C')
        return to_qimage(background)

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
    db_client = GridMongoClient()

    main_window = ApplicationWindow(grid, palette, db_client)
    author_string = 'LUT Color Correction - made by Alexander Tsukanov'
    main_window.setWindowTitle(author_string)
    main_window.setCentralWidget(DragAndDropCanvas(grid, palette, parent=main_window))
    main_window.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    start()
