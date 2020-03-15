from drafter.utils.rect import default_rect
from drafter.utils.pos_size import Position, calc_size, calc_rect_size


class Node:
    children = []
    background = None
    width, height = None, None
    margin = default_rect
    padding = default_rect
    position = Position.STATIC
    max_draw_pass = 1

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def draw_content(self, ctx, x, y, w, h):
        if self.background is None:
            return w, h
        ctx.rectangle(x, y, w, h)
        ctx.set_source_rgba(*self.background)
        ctx.fill()

        return w, h

    def pre_update(self, context, child_context, draw_pass):
        pass

    def update(self, context, child_context, child_response, draw_pass):
        parent = child_context['parent']
        parent['rx'] += child_response['dx']

    def pre_draw(self, context, draw_pass):
        pass

    def post_draw(self, context, draw_pass):
        pass

    def draw(self, context, draw_pass=1, dirty=False):
        self.pre_draw(context, draw_pass)

        parent = context['parent']
        abs_parent = context['abs_parent']
        if self.position == Position.ABSOLUTE:
            pos_x = abs_parent['x']
            pos_y = abs_parent['y']
        else:
            pos_x = parent['x'] + parent['rx']
            pos_y = parent['y'] + parent['ry']

        margin = calc_rect_size(parent['w'], parent['h'], self.margin)
        x = pos_x + margin.left
        y = pos_y + margin.top

        w = calc_size(parent['w'], self.width)
        h = calc_size(parent['h'], self.height)

        ctx = context['ctx']
        dirty_ctx = context['dirty_ctx']

        dirty = dirty or (draw_pass < self.max_draw_pass)
        if dirty:
            w, h = self.draw_content(dirty_ctx, x, y, w, h)
        else:
            w, h = self.draw_content(ctx, x, y, w, h)

        this_parent = {
            'w': w,
            'h': h,
            'x': x,
            'y': y,
            'rx': 0,
            'ry': 0,
        }
        child_context = {
            **context,
            'parent': this_parent,
            'abs_parent': (
                this_parent if
                self.position in [Position.ABSOLUTE, Position.RELATIVE]
                else abs_parent
            )
        }

        self.pre_update(context, child_context, draw_pass)
        for c in self.children:
            child_response = c.draw(child_context, 1, dirty)
            self.update(context, child_context, child_response, draw_pass)

        self.post_draw(context, draw_pass)

        if draw_pass < self.max_draw_pass:
            this_parent['rx'] = 0
            this_parent['ry'] = 0
            self.last_pass_context = child_context
            return self.draw(context, draw_pass + 1)

        if self.position == Position.ABSOLUTE:
            return {
                'dx': 0,
                'dy': 0,
            }
        else:
            return {
                'dx': w + margin.left + margin.right,
                'dy': h + margin.top + margin.bottom,
            }
