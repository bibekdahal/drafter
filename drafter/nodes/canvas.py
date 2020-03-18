# canvas.py
# Author: Bibek Dahal

from drafter.node import Node


def draw(ctx, w, h):
    """
    Default callback for a canvas. Does nothing.
    """
    return w, h


class Canvas(Node):
    """
    A canvas is a rectangular area where the user can use the cairo
    context to draw anything.

    Properties:
    draw_callback: Function called to draw in the canvas.
    """
    draw_callback = draw

    def draw_content(self, ctx, x, y, w, h):
        """
        Use the callback to draw whatever the user likes and translate it
        to the position (x, y).
        """
        ctx.save()
        ctx.translate(x, y)
        w, h = self.draw_callback(ctx, w, h)
        ctx.restore()
        return w, h
