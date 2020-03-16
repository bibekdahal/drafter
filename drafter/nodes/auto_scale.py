from drafter.node import Node


class AutoScale(Node):
    max_draw_pass = 2
    horizontal = True
    vertical = True

    def pre_draw(self, context, draw_pass):
        if draw_pass == 1:
            return

        me = self.last_pass_context['parent']
        tw, th = me['w'], me['h']
        cw, ch = self.children_width, self.children_height
        sx, sy = 1, 1

        if self.horizontal:
            sx = tw / cw if tw < cw else 1
        if self.vertical:
            sy = th / ch if th < ch else 1

        ctx = context['ctx']
        ctx.save()
        ctx.scale(sx, sy)

    def post_draw(self, context, draw_pass):
        if draw_pass == 1:
            return

        ctx = context['ctx']
        ctx.restore()
