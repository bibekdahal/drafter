import cairo


class Report():
    def __init__(self, filename, width, height):
        self.filename = filename
        self.width = width
        self.height = height

    def get_surface(self, filename, width, height):
        raise NotImplementedError

    def finish_drawing(self, surface, filename):
        raise NotImplementedError

    def draw_page(self, root_node):
        surface = self.get_surface(self.filename, self.width, self.height)
        dirty_surface = self.get_surface(None, self.width, self.height)

        ctx = cairo.Context(surface)
        dirty_ctx = cairo.Context(dirty_surface)

        body = {
            'w': 256,
            'h': 256,
            'x': 0,
            'y': 0,
            'rx': 0,
            'ry': 0,
        }
        root_node.draw({
            'ctx': ctx,
            'dirty_ctx': dirty_ctx,
            'parent': body,
            'abs_parent': body
        })

        self.finish_drawing(surface, self.filename)


class PngReport(Report):
    def get_surface(self, filename, width, height):
        return cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    def finish_drawing(self, surface, filename):
        surface.write_to_png(filename)


class PdfReport(Report):
    def get_surface(self, filename, width, height):
        return cairo.PDFSurface(filename, width, height)

    def finish_drawing(self, surface, filename):
        surface.show_page()
