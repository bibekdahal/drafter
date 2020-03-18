import cairo
from drafter.utils.color import parse_color


class Border:
    CAP_BUTT = cairo.LINE_CAP_BUTT
    CAP_ROUND = cairo.LINE_CAP_ROUND
    CAP_SQUARE = cairo.LINE_CAP_SQUARE

    def __init__(
        self,
        radius=0,
        width=0,
        color=[0, 0, 0, 1],
        line_cap=CAP_SQUARE,
        line_dash=[],
    ):
        self.radius = radius
        self.width = width
        self.color = parse_color(color)
        self.line_cap = line_cap
        self.line_dash = line_dash

    def draw(self, ctx, x, y, w, h, preserve=True):
        if self.width == 0:
            return

        # TODO: Fix to draw in the inner rectangle.
        r = self.radius
        ctx.move_to(x+r, y)
        ctx.line_to(x+w-r, y)
        ctx.curve_to(x+w, y, x+w, y, x+w, y+r)
        ctx.line_to(x+w, y+h-r)
        ctx.curve_to(x+w, y+h, x+w, y+h, x+w-r, y+h)
        ctx.line_to(x+r, y+h)
        ctx.curve_to(x, y+h, x, y+h, x, y+h-r)
        ctx.line_to(x, y+r)
        ctx.curve_to(x, y, x, y, x+r, y)

        ctx.set_line_width(self.width)
        ctx.set_source_rgba(*self.color)
        ctx.set_dash(self.line_dash)
        ctx.set_line_cap(self.line_cap)

        if preserve:
            ctx.stroke_preserve()
        else:
            ctx.stroke()
