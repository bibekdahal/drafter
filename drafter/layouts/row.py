from drafter.node import Node


class Row(Node):
    align = 'start'
    justify = 'start'

    def update_layout(self):
        # When update_layout is called, self's x and y are already set
        # but we may need to find w and h.
        # We also need to find x, y and possible w, h of children.

        self.calculate_layout()

        # We are ready to caculate absolute layout of children
        for c in self.children:
            if c.absolute:
                c.update_absolute_layout()

        non_absolute_children = [
            c for c in self.children if not c.absolute
        ]

        if len(non_absolute_children) == 0:
            return

        if self.w is None:
            # If w is not known, calculate it as total of children's w.
            # Also, we cannot actually justify children,
            # so justify at the start.
            w = 0
            x = self.x
            for c in non_absolute_children:
                c.x = x + c.margin.left
                c.update_layout()
                if c.w is None:
                    raise Exception('Node layout cannot be calculated')

                x += c.w + c.margin.spacing_x()
                w = c.x + c.w + c.margin.spacing_x()
            self.w = w

        for c in self.children:
            c.update_layout()

        # Next calculate x of children based on justify
        total_w = sum([
            c.w + c.margin.spacing_x()
            for c in non_absolute_children
            if c.w is not None
        ])

        if self.justify == 'end':
            x = self.x + self.w - total_w
        elif self.justify == 'center':
            x = self.x + self.w / 2 - total_w / 2
        else:
            x = self.x

        for c in non_absolute_children:
            c.x = x + c.margin.left
            if c.w:
                x += c.w + c.margin.spacing_x()

        # Now do similar to h
        if self.h is None:
            h = 0
            y = self.y
            for c in non_absolute_children:
                c.y = y + c.margin.top
                c.update_layout()
                if c.h is None:
                    raise Exception('Node layout cannot be calculated')

                h = c.y + c.h + c.margin.spacing_y()
            self.h = h

        for c in self.children:
            c.update_layout()

        if self.align == 'end':
            y = self.y + self.h
        elif self.align == 'center':
            y = self.y + self.h / 2
        else:
            y = self.y

        for c in non_absolute_children:
            if self.align == 'center' and c.h:
                c.y = y - c.h / 2
            elif self.align == 'end' and c.h:
                c.y = y - c.h - c.margin.bottom
            else:
                c.y = y + c.margin.top

        for c in self.children:
            c.update_layout()