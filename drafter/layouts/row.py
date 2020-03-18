# row.py
# Author: Bibek Dahal

from drafter.node import Node
from drafter.utils.pos_size import Justify, Align


class Row(Node):
    """
    Represents a horizontal layout of children.

    Properties:
    * justify: One of (START, SPACE_BETWEEN, SPACE_AROUND, END)
               to arrange the children over the width of this node.
    * align: One of (START, CENTER, END) to arrange the children
             over the height of this node.
    """
    justify = Justify.START
    align = Align.START

    # We need at least 2 drawing passes for this node to work.
    min_draw_pass = 2

    def pre_draw(self, context, draw_pass, dirty):
        """
        When we are in the second drawing pass, we know the size of each child.
        Use that knowledge to calculate the x-spacing required between the
        children.
        """
        if draw_pass == 1:
            self.children_heights = []
            return

        me = self.last_pass_context['parent']
        total_width = me['w']

        if self.justify == Justify.SPACE_BETWEEN:
            divisor = len(self.children) - 1
            self.spacing = (total_width - self.children_width) / divisor
        elif self.justify == Justify.SPACE_AROUND:
            divisor = len(self.children) + 1
            self.spacing = (total_width - self.children_width) / divisor
        elif self.justify == Justify.END:
            self.spacing = total_width - self.children_width

    def pre_update(self, context, child_context, draw_pass):
        """
        pre_update is called before drawing any child.
        In the second drawing pass,
        the relative x position of the first child should be updated for
        justify = SPACE_AROUND and justify = END.
        """
        if draw_pass == 1:
            return

        me = child_context['parent']
        if self.justify == Justify.SPACE_AROUND:
            me['rx'] += self.spacing

        elif self.justify == Justify.END:
            me['rx'] += self.spacing

        self.child = 0
        if self.align == Align.CENTER:
            me['ry'] = (me['h'] - self.children_heights[self.child]) / 2
        elif self.align == Align.END:
            me['ry'] = me['h'] - self.children_heights[self.child]

    def update(self, context, child_context, child_response, draw_pass):
        """
        update is called after drawing each child.
        In the second drawing pass,
        the relative x position of the next child should be updated for
        justify = SPACE_BETWEEN and justify = SPACE_AROUND using `spacing`
        and the rest without any spacing.
        """

        me = child_context['parent']
        if draw_pass == 1:
            me['rx'] += child_response['dx']
            self.children_heights.append(child_response['dy'])
            return

        if self.justify in [Justify.SPACE_BETWEEN, Justify.SPACE_AROUND]:
            me['rx'] += child_response['dx'] + self.spacing
        else:
            me['rx'] += child_response['dx']

        self.child += 1
        if self.child == len(self.children):
            return
        if self.align == Align.CENTER:
            me['ry'] = (me['h'] - self.children_heights[self.child]) / 2
        elif self.align == Align.END:
            me['ry'] = me['h'] - self.children_heights[self.child]
