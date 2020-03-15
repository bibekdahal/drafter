from drafter.node import Node


class AutoScale(Node):
    max_draw_pass = 2
    horizontal = True
    vertical = True

    def pre_draw(self, context, draw_pass):
        if draw_pass == 1:
            self.child_width = 0
            self.child_height = 0
            return

        me = self.last_pass_context['parent']
        tw, th = me['w'], me['h']
        cw, ch = self.child_width, self.child_height
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

    def update(self, context, child_context, child_response, draw_pass):
        self.child_width += child_response['dx']
        self.child_height += child_response['dy']
        super().update(context, child_context, child_response, draw_pass)
