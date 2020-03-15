from drafter.node import Node


def draw(ctx, w, h):
    return w, h


class Canvas(Node):
    draw_callback = draw

    def draw_content(self, ctx, x, y, w, h):
        ctx.save()
        ctx.translate(x, y)
        w, h = self.draw_callback(ctx, w, h)
        ctx.restore()
        return w, h
