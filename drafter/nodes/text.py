import gi
gi.require_version('Pango', '1.0')  # noqa
gi.require_version('PangoCairo', '1.0')  # noqa

from gi.repository import Pango, PangoCairo
from drafter.node import Node
from drafter.utils.font import get_font_desc


class Text(Node):
    text = None
    color = [0, 0, 0, 1]

    WORD_WRAP = Pango.WrapMode.WORD
    CHAR_WRAP = Pango.WrapMode.WORD_CHAR
    WORD_CHAR_WRAP = Pango.WrapMode.WORD_CHAR

    NORMAL = Pango.Weight.NORMAL
    BOLD = Pango.Weight.BOLD

    LEFT = Pango.Alignment.LEFT
    CENTER = Pango.Alignment.CENTER
    RIGHT = Pango.Alignment.RIGHT
    JUSTIFY = 99

    TOP = 9090
    MIDDLE = 9099
    BOTTOM = 9900

    wrap_mode = WORD_WRAP
    alignment = LEFT
    vertical_alignment = TOP
    line_spacing = None

    markup = True
    font_family = 'Arial'
    font_size = 8
    font_weight = None

    def draw_content(self, ctx, x, y, w, h):
        ctx.save()
        ctx.identity_matrix()
        layout = PangoCairo.create_layout(ctx)
        ctx.restore()

        layout.set_font_description(get_font_desc(
            self.font_family, self.font_size, self.font_weight
        ))

        if self.alignment == Text.JUSTIFY:
            layout.set_alignment(Text.LEFT)
            layout.set_justify(True)
        else:
            layout.set_alignment(self.alignment)

        if self.line_spacing is not None:
            layout.set_spacing(self.line_spacing * Pango.SCALE)

        if self.markup:
            layout.set_markup(str(self.text), -1)
        else:
            layout.set_text(str(self.text), -1)

        if not w:
            layout.set_width(-1)
        else:
            layout.set_width(w * Pango.SCALE)
        layout.set_wrap(self.wrap_mode)

        if h:
            layout.set_height(h * Pango.SCALE)

        extents = layout.get_extents()[1]
        extents = [
            extents.width / Pango.SCALE,
            extents.height / Pango.SCALE,
        ]
        ctx.save()

        if h:
            if self.vertical_alignment == Text.BOTTOM:
                ctx.translate(x, y + h - extents[1])
            elif self.vertical_alignment == Text.MIDDLE:
                ctx.translate(x, y + h / 2 - extents[1] / 2)
            else:
                ctx.translate(x, y)
        else:
            ctx.translate(x, y)
        ctx.set_source_rgba(*self.color)
        PangoCairo.show_layout(ctx, layout)
        ctx.restore()

        return extents[0], extents[1]
