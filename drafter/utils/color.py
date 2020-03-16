import colorsys


def rgb(r, g, b):
    return [
        r / 255,
        g / 255,
        b / 255,
        1,
    ]


def rgba(r, g, b, a):
    return [
        r / 255,
        g / 255,
        b / 255,
        a,
    ]


def hsl(h, s, l):
    return rgb(*colorsys.hls_to_rgb(h, l, s))


def hsla(h, s, l, a):
    return rgba(*colorsys.hls_to_rgb(h, l, s), a)


def hx(hexstr):
    h = hexstr.lstrip('#')
    if len(h) == 3:
        h = f'{h[0]}{h[0]}{h[1]}{h[1]}{h[2]}{h[2]}'
    rgb_t = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return rgb(*rgb_t)


def parse_color(color):
    if isinstance(color, list):
        if len(color) == 3:
            return [*color, 1]
        if len(color) != 4:
            raise Exception(f'Invalid number of color components in: {color}')
        return color

    if isinstance(color, str):
        if color[0] == '#' and len(color) == 7 or len(color) == 4:
            return hx(color)
        elif color[:4] == 'rgb(' and color[-1] == ')':
            return rgb(*[
                float(x) for x in color[4:-1].split(',')
            ])
        elif color[:5] == 'rgba(' and color[-1] == ')':
            return rgba(*[
                float(x) for x in color[5:-1].split(',')
            ])
        elif color[:4] == 'hsl(' and color[-1] == ')':
            return hsl(*[
                float(x) for x in color[4:-1].split(',')
            ])
        elif color[:5] == 'hsla(' and color[-1] == ')':
            return hsla(*[
                float(x) for x in color[5:-1].split(',')
            ])

    raise Exception(f'Invalid color: {color}')
