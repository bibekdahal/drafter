from drafter.utils.rect import default_rect
from drafter.utils.pos_size import Position, calc_size, calc_rect_size
from drafter.utils.color import parse_color


class Node:
    children = []
    background = None
    width, height = None, None
    margin = default_rect
    padding = default_rect
    border = None
    position = Position.STATIC
    max_draw_pass = 1

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def draw_border_and_background(self, ctx, x, y, w, h):
        xx = x + self.padding.left
        yy = y + self.padding.top
        ww = w - self.padding.left - self.padding.right
        hh = h - self.padding.top - self.padding.bottom

        ctx.save()
        ctx.identity_matrix()

        if self.background is not None:
            ctx.rectangle(x, y, w, h)
            ctx.set_source_rgba(*parse_color(self.background))
            ctx.fill()

        if self.border is not None:
            self.border.draw(ctx, x, y, w, h)

        ctx.restore()
        return xx, yy, ww, hh

    def draw_content(self, ctx, x, y, w, h):
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
        """
        Drawing can occur in several passes to establish the final layout.

        Following are the cases when multiple drawing passes can occur:

        - This is the first pass but the width or height of this node
          is not known. In such a case, we render all the content and the
          children and save their total width/height for the next pass.
          This width/height is necessary for drawing background, border as
          well as may be necessary for this node's parent.

         - This node always requires two passes. For example, to justify
           content between children nodes in the 'Row' node or to
           fit the content in the 'AutoScale' node. Both of these cases
           require the size of the children, so the children need to be drawn
           in the first pass.
         """

        # We are drawing either with respect to immediate parent
        # or with respect to the nearest absolute parent.
        parent = context['parent']
        abs_parent = context['abs_parent']

        # Based on `position` property, set where to draw this node.
        if self.position == Position.ABSOLUTE:
            pos_x = abs_parent['x']
            pos_y = abs_parent['y']
        else:
            pos_x = parent['x'] + parent['rx']
            pos_y = parent['y'] + parent['ry']

        # Make sure to consider margin when finding this node's position.
        margin = calc_rect_size(parent['w'], parent['h'], self.margin)
        x = pos_x + margin.left
        y = pos_y + margin.top

        if draw_pass > 1:
            # If this is not the first pass, then for width and height,
            # we will consider the final width and height of the last pass.
            w = self.last_pass_context['parent']['w']
            h = self.last_pass_context['parent']['h']
        else:
            # Otherwise, simply set width and height to whatever the user
            # has chosen.
            w = calc_size(parent['w'], self.width)
            h = calc_size(parent['h'], self.height)

        # If this is not the first pass, we do not want to draw in the
        # TRUE surface but rather in the DIRTY surface. Grab cairo contexts for
        # both the surfaces.
        ctx = context['ctx']
        dirty_ctx = context['dirty_ctx']

        # Are we in the first pass but width and height are unknown?
        width_undetected = (draw_pass == 1) and not w
        height_undetected = (draw_pass == 1) and not h
        size_undetected = width_undetected or height_undetected

        # We will draw in the dirty surface in 2 cases:
        # - Our parent is drawing in the dirty surface, so dirty = True
        # - This is not the first pass, either because this node requires
        #   more passes or because width or height of this node is not known.
        dirty = dirty or (draw_pass < self.max_draw_pass) or size_undetected

        # Before drawing,
        # if the specific node wants to do something, do it here.
        self.pre_draw(context, draw_pass)

        if dirty:
            # Drawing on the dirty surface.
            # Make sure to grab the returned width and height
            # as these can be useful in the subsequent passes.
            w, h = self.draw_content(dirty_ctx, x, y, w, h)
        else:
            # Drawing on the true surface.
            # First we draw border and background.
            # Note that x, y, w, h are modified to consider padding.
            x, y, w, h = self.draw_border_and_background(ctx, x, y, w, h)
            # Then draw the actual content.
            w, h = self.draw_content(ctx, x, y, w, h)

        # `parent` context for the children nodes.
        this_parent = {
            'w': w,
            'h': h,
            'x': x,
            'y': y,
            'rx': 0,  # Relative position for each child to draw.
            'ry': 0,  # Relative position for each child to draw.
        }

        # Create the context for the children nodes.
        child_context = {
            **context,              # All values are same except:
            'parent': this_parent,  # The parent.
            'abs_parent': (         # And, possibly the absolute parent.
                this_parent if
                self.position in [Position.ABSOLUTE, Position.RELATIVE]
                else abs_parent
            )
        }

        # Any updates to do before rendering the children?
        self.pre_update(context, child_context, draw_pass)

        # Let's save the total children width and height for subsequent passes.
        self.children_width = 0
        self.children_height = 0
        for c in self.children:
            # Draw each child.
            child_response = c.draw(child_context, 1, dirty)
            # Update total children size based on the returned values.
            self.children_width += child_response['dx']
            self.children_height += child_response['dy']

            # Possibly, update the context for next child.
            # The main operation in this method is to update the relative
            # position.
            self.update(context, child_context, child_response, draw_pass)

        # After everything is drawn,
        # if the specific node wants to do something, do it here.
        self.post_draw(context, draw_pass)

        # If a size was previously unknown
        # and this is the first pass, we will save the content/children size
        # for subsequent passes.
        if width_undetected:
            this_parent['w'] = max(w, self.children_width)
        if height_undetected:
            this_parent['h'] = max(h, self.children_height)

        # If we need to draw another pass, draw it.
        if draw_pass < self.max_draw_pass or size_undetected:
            self.last_pass_context = child_context
            return self.draw(context, draw_pass + 1)

        # Return the total space taken by this child.
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
