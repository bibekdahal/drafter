from drafter.node import Node
from drafter.utils.pos_size import Justify


class Row(Node):
    justify = Justify.START
    max_draw_pass = 2

    def pre_update(self, context, child_context, draw_pass):
        if draw_pass == 1:
            return

        me = child_context['parent']
        if self.justify == Justify.SPACE_AROUND:
            me['rx'] += self.spacing

        elif self.justify == Justify.END:
            me['rx'] += self.spacing

    def update(self, context, child_context, child_response, draw_pass):
        me = child_context['parent']
        if draw_pass > 1:
            if self.justify in [Justify.SPACE_BETWEEN, Justify.SPACE_AROUND]:
                me['rx'] += child_response['dx'] + self.spacing
                return

        me['rx'] += child_response['dx']
        self.children_w.append(child_response['dx'])

    def pre_draw(self, context, draw_pass):
        if draw_pass == 1:
            self.children_w = []
            return

        me = self.last_pass_context['parent']
        total_width = me['w']
        children_width = sum(self.children_w)

        if self.justify == Justify.SPACE_BETWEEN:
            divisor = len(self.children_w) - 1
            self.spacing = (total_width - children_width) / divisor
        elif self.justify == Justify.SPACE_AROUND:
            divisor = len(self.children_w) + 1
            self.spacing = (total_width - children_width) / divisor
        elif self.justify == Justify.END:
            self.spacing = total_width - children_width
