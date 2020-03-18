from drafter.utils.rect import Rect


class Justify:
    START = 0
    SPACE_BETWEEN = 1
    SPACE_AROUND = 2
    END = 3


class Align:
    START = 0
    CENTER = 1
    END = 2


class Position:
    STATIC = 0
    ABSOLUTE = 1
    RELATIVE = 2


def calc_size(parent_size, size, default_size=0):
    if parent_size is None:
        parent_size = 0
    if size is None:
        if callable(default_size):
            return default_size()
        return default_size
    if isinstance(size, str) and size[-1] == '%':
        return float(size[:-1]) / 100 * parent_size
    return float(size)


def calc_rect_size(parent_w, parent_h, size, default_size=0):
    return Rect(
        calc_size(parent_h, size.top, default_size),
        calc_size(parent_w, size.right, default_size),
        calc_size(parent_h, size.bottom, default_size),
        calc_size(parent_w, size.left, default_size)
    )
