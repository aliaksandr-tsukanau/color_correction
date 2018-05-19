import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget

from grid.grid_instance import grid
from image.image import correct_image

import pprint


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
        self.setGeometry(0, 0, grid.radius * 2, grid.radius * 2)

        self._pen_pinned = QPen(Qt.black, 10, Qt.SolidLine)
        self._pen_notpinned = QPen(Qt.black, 5, Qt.SolidLine)
        self._pen_edge = QPen(Qt.black, 1, Qt.SolidLine)

        self._update_nodes_array()

    def _update_nodes_array(self):
        """writes numpy array of all grid's nodes to instance field self._nodes"""
        self._nodes = np.array([node.coords_for_canvas for node in grid.nodes()])
        # nodes are stored as a numpy copy to simplify and fasten calculations of distances

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self._update_nodes_array()  # copy changes of branch update inside this class
        self.draw_points(painter)
        self.draw_edges(painter)
        painter.end()

    def draw_points(self, painter: QPainter):
        for i, (x, y) in enumerate(self._nodes):
            painter.setPen(
                self._pen_pinned if grid[i].is_pinned else self._pen_notpinned)
            painter.drawPoint(x, y)

    def draw_edges(self, painter: QPainter):
        painter.setPen(self._pen_edge)

        # radial edges
        for branch in grid.branches:
            for from_, to in zip(branch.nodes, branch.nodes[1:]):
                painter.drawLine(*from_.coords_for_canvas, *to.coords_for_canvas)

        # concentric edges
        nodes_per_branch = len(grid.branches)
        for i in range(nodes_per_branch):
            for branch_from, branch_to in zip(grid.branches, grid.branches[1:] + [grid.branches[0]]):
                painter.drawLine(
                                *branch_from.nodes[i].coords_for_canvas,
                                *branch_to.nodes[i].coords_for_canvas
                                 )

    def _get_mouse_position(self, evt):
        return np.array([evt.pos().x(), evt.pos().y()])

    def mousePressEvent(self, evt):
        if evt.button() == Qt.LeftButton and self.draggin_idx is None:
            point = self._get_mouse_position(evt)

            def _get_clicked_node_idx():
                # dist will hold the square distance from the click to the points
                dist = self._nodes - point
                dist = dist[:, 0] ** 2 + dist[:, 1] ** 2
                dist[dist > self._delta] = np.inf  # obviate the distances above DELTA
                if dist.min() < np.inf:
                    return dist.argmin()
                else:
                    return None
            self.draggin_idx = _get_clicked_node_idx()

    def _redraw_to_new_mouse_position(self, evt):
        point = self._get_mouse_position(evt)
        self._nodes[self.draggin_idx] = point

        node_to_update = grid[int(self.draggin_idx)]
        # int() call is required since islice inside Grid.__getattr__()
        # does not accept numpy index
        node_to_update.update_grid(*point)

        self.update()

    def mouseMoveEvent(self, evt):
        if self.draggin_idx is not None:
            self._redraw_to_new_mouse_position(evt)

    def mouseReleaseEvent(self, evt):
        if evt.button() == Qt.LeftButton and self.draggin_idx is not None:
            self._redraw_to_new_mouse_position(evt)
            self.draggin_idx = None

