import sys

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow

from Color.color_spaces import RGB_BACKGROUND
from Grid.grid_instance import grid
from Gui.canvas import DragAndDropCanvas
from Image.to_qimage import to_qimage


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(500)
        self.setFixedHeight(500)

    def paintEvent(self, e):
        painter = QPainter(self)

        background = RGB_BACKGROUND
        qimage = to_qimage(background)
        painter.drawImage(QRect(0, 0, 500, 500), qimage)

        # painter.setPen(QPen(Qt.black, 10, Qt.SolidLine))
        #
        # g = Grid(10, 250)
        # for branch in g.branches:
        #     for node in branch.nodes:
        #         painter.drawPoint(node.x + 250, node.y + 250)


def start():
    application = QApplication(sys.argv)
    main_window = ApplicationWindow()
    main_window.setCentralWidget(DragAndDropCanvas(None, grid))
    main_window.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    start()
