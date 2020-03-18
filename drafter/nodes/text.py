# text.py
# Author: Bibek Dahal

import gi
gi.require_version('Pango', '1.0')  # noqa
gi.require_version('PangoCairo', '1.0')  # noqa

from gi.repository import Pango, PangoCairo
from drafter.node import Node
from drafter.utils.font import get_font_desc
from drafter.utils.color import parse_color


class Text(Node):
    """
    Represents a text content.

    Properties:
    * text: Text to draw.
    * color: Font color for the text.
    * wrap_mode: One of (WORD_WRAP, CHAR_WRAP, WORD_CHAR_WRAP).
    * alignment: One of (LEFT, CENTER, RIGHT, JUSTIFY).
    * vertical_algignment: One of (TOP, MIDDLE, BOTTOM).
    * line_spacing: Spacing between lines.
    * markup: True/False indicating whether the text is a Pango markup.
    * font_family: Font family to render the text with.
    * font_size: Font size of the text.
    * font_weight: One of (NORMAL, BOLD).
    """

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

    text = None
    color = [0, 0, 0, 1]

    wrap_mode = WORD_WRAP
    alignment = LEFT
    vertical_alignment = TOP
    line_spacing = None

    markup = True
    font_family = 'Arial'
    font_size = 8
    font_weight = NORMAL

    def draw_content(self, ctx, x, y, w, h):
        """
        Draw the text using Pango.

        Note that cairo and pango has different units, so need to use
        Pango.SCALE in numeric values below.
        """

        # First create a Pango layout.
        # Any existing transformation can affect the layout, so
        # reset the transformation when creating the layout.
        ctx.save()
        ctx.identity_matrix()
        layout = PangoCairo.create_layout(ctx)
        ctx.restore()

        # Set the font description.
        layout.set_font_description(get_font_desc(
            self.font_family, self.font_size, self.font_weight
        ))

        # Set the horizontal alignment.
        if self.alignment == Text.JUSTIFY:
            layout.set_alignment(Text.LEFT)
            layout.set_justify(True)
        else:
            layout.set_alignment(self.alignment)

        # Set line spacing.
        if self.line_spacing is not None:
            layout.set_spacing(self.line_spacing * Pango.SCALE)

        # Set the text content. If using markup, use set_markup.
        if self.markup:
            layout.set_markup(str(self.text), -1)
        else:
            layout.set_text(str(self.text), -1)

        # If width is zero or unset (None is most probably converted to zero),
        # set the width to -1 to auto-resize the layout.
        # Else set the width provided.
        if not w:
            layout.set_width(-1)
        else:
            layout.set_width(w * Pango.SCALE)

        # Wrap mode when width is limited.
        layout.set_wrap(self.wrap_mode)

        # Height.
        layout.set_height(h * Pango.SCALE)

        # Get the actual width and height of the layout based on text content.
        extents = layout.get_extents()[1]
        extents = [
            extents.width / Pango.SCALE,
            extents.height / Pango.SCALE,
        ]

        # To draw at given position, we will use the translate function.
        # So need to save the cairo context before doing that.
        ctx.save()
        # Translate to the given x and y position.
        # Based on the vertical alignment, the y position can vary.
        if h:
            if self.vertical_alignment == Text.BOTTOM:
                y = y + h - extents[1]
            elif self.vertical_alignment == Text.MIDDLE:
                y = y + h / 2 - extents[1] / 2
        ctx.translate(x, y)

        # Set the font color.
        ctx.set_source_rgba(*parse_color(self.color))
        # Draw the text.
        PangoCairo.show_layout(ctx, layout)

        # Restore the cairo context.
        ctx.restore()

        # Return the actual width and height of the text content.
        return max(w, extents[0]), max(h, extents[1])
