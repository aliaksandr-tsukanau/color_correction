#  Copyright (c) 2018 Aliaksandr Tsukanau.
#  Licensed under GNU General Public Licence, version 3.
#  You may not use this file except in compliance with GNU General Public License, version 3.
#  See the GNU General Public License, version 3 for more details. https://www.gnu.org/licenses/gpl-3.0.en.html
#

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
