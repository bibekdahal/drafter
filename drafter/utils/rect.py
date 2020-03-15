
class Rect:
    def __init__(self, top, right=None, bottom=None, left=None):
        if right is None:
            self.top, self.right, self.bottom, self.left = top, top, top, top
        elif bottom is None:
            self.top, self.bottom = top, top
            self.right, self.left = right, right
        elif left is None:
            self.top = top
            self.right, self.left = left, left
            self.bottom = bottom
        else:
            self.top = top
            self.right = right
            self.bottom = bottom
            self.left = left


default_rect = Rect(0)
