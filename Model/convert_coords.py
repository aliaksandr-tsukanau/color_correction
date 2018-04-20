from collections import namedtuple


Line = namedtuple('Line', 'start_x start_y end_x end_y')


def zerocentered_to_pyqt(model_line: Line, offset=200) -> Line:
    """Converts coordinates of a line from (0, 0)-centered form to PyQt form
    line - namedtuple of form (start_x, start_y, finish_x, finish_y)"""
    return Line((coord + offset for coord in model_line))
