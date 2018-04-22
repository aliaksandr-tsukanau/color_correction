import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget

from grid.grid_instance import grid


# TODO: not allow nodes go out of canvas
# TODO: fix center behaviour

class DragAndDropCanvas(QWidget):
    """Custom canvas (QPainter-like) widget that supports dragging of nodes by mouse"""

    def __init__(self, parent=None, delta=30):
        """delta - minimum distance at which node reacts to mouse dragging\
        (actually square distance).
        Affects grid sensitivity"""
        super().__init__(parent)
        self._delta = delta
        self.draggin_idx = None
        self.setGeometry(0, 0, 500, 500)

        self._grid = grid

        self._nodes = np.array([node.coords_for_canvas for node in grid.nodes()])

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

            if self.draggin_idx is not None:
                node_to_update = grid[int(self.draggin_idx)]
                # int() call is required since islice inside Grid.__getattr__()
                # does not accept numpy index
            node_to_update.x = point[0]
            node_to_update.y = point[1]

            self.draggin_idx = None
            self.update()

