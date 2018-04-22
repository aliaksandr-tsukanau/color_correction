from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication
import numpy as np
from Model.grid import Grid


class DragAndDropCanvas(QWidget):
    """Custom canvas (QPainter-like) widget that supports dragging of nodes by mouse"""

    def __init__(self, parent, grid, delta=30):
        """delta - minimum distance at which node reacts to mouse dragging (actually square distance)"""
        super().__init__(parent)
        self._delta = delta
        self.draggin_idx = None
        self.setGeometry(0, 0, 500, 500)

        self._grid = grid
        branches = grid.branches
        nodes = []
        for branch in branches:
            nodes += branch.nodes

        self._nodes = np.array([[node.x + 250, node.y + 250] for node in nodes])

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_points(qp)
        qp.end()

    def draw_points(self, qp):
        qp.setPen(QPen(Qt.black, 10, Qt.SolidLine))
        for x, y in self._nodes:
            qp.drawPoint(x, y)

    def _get_point(self, evt):
        return np.array([evt.pos().x(), evt.pos().y()])

    # get the click coordinates
    def mousePressEvent(self, evt):
        if evt.button() == Qt.LeftButton and self.draggin_idx is None:
            point = self._get_point(evt)
            # dist will hold the square distance from the click to the points
            dist = self._nodes - point
            dist = dist[:, 0]**2 + dist[:, 1]**2
            dist[dist > self._delta] = np.inf  # obviate the distances above DELTA
            if dist.min() < np.inf:
                self.draggin_idx = dist.argmin()

    def mouseMoveEvent(self, evt):
        if self.draggin_idx is not None:
            point = self._get_point(evt)
            self._nodes[self.draggin_idx] = point
            self.update()

    def mouseReleaseEvent(self, evt):
        if evt.button() == Qt.LeftButton and self.draggin_idx is not None:
            point = self._get_point(evt)
            self._nodes[self.draggin_idx] = point
            self.draggin_idx = None
            self.update()

app = QApplication([])
c = DragAndDropCanvas(parent=None, grid=Grid(branches_number=8, radius=250))
c.show()
app.exec_()
