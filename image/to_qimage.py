from PyQt5.QtGui import QImage, qRgb
import numpy as np


GRAY_COLOR_TABLE = [qRgb(i, i, i) for i in range(256)]


def to_qimage(im, copy=False):
    """converts image from np array of shape (..., ..., 3)\
    with color values of type uint8 in range [0; 255] to QImage for PyQt"""
    if im is None:
        return QImage()

    if im.dtype == np.uint8 and im.shape[2] == 3:
        qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
        return qim.copy() if copy else qim

    raise ValueError('Input array must be an np array of shape (..., ..., 3) with elements of type uint8.')
