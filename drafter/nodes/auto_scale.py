# auto_scale.py
# Author: Bibek Dahal

from drafter.node import Node


class AutoScale(Node):
    """
    Auto scales the children so that they fit in this node perfectly.

    Properties:
    horizontal: True/False indicating whether to resize horizontally.
    vertical: True/False indicating whether to resize vertically.
    """
    horizontal = True
    vertical = True

    # Needs at least two drawing passes.
    min_draw_pass = 2

    def pre_update(self, context, child_context, draw_pass):
        """
        In the second drawing pass, we will scale the cairo context
        using the size of this node and the total size of the children
        so that all children are fit to this container.
        """
        if draw_pass == 1:
            return

        # Get our width and height from the previous pass.
        me = self.last_pass_context['parent']
        tw, th = me['w'], me['h']
        # Get the children width and height.
        cw, ch = self.children_width, self.children_height

        # Scaling is by default 1, 1
        # It is less than 1 if total size is less than children size.
        sx = tw / cw if self.horizontal and tw < cw else 1
        sy = th / ch if self.vertical and th < ch else 1

        # Scale the context.
        ctx = context['ctx']
        ctx.save()
        ctx.translate(me['x'], me['y'])
        ctx.scale(sx, sy)
        ctx.translate(-me['x'], -me['y'])

    def post_draw(self, context, draw_pass, dirty):
        """
        After everything is drawn, in the second pass, we want to reset the
        scaling that was
        """
        if draw_pass == 1:
            return

        ctx = context['ctx']
        ctx.restore()
