import gi
gi.require_version('Pango', '1.0')  # noqa
gi.require_version('PangoCairo', '1.0')  # noqa
from gi.repository import Pango, PangoCairo


def get_font_desc(font_family, font_size, font_weight):
    font_map = PangoCairo.font_map_get_default()
    desc = next((
        v.list_faces()[0].describe() for v in font_map.list_families()
        if font_family.lower() in v.get_name().lower()
    ), None)  # TODO Default font

    if desc is None:
        return None

    desc.set_style(Pango.Style.NORMAL)
    desc.set_weight(Pango.Weight.NORMAL)

    if font_size is not None:
        desc.set_size(font_size * Pango.SCALE)

    if font_weight is not None:
        desc.set_weight(font_weight)

    return desc
