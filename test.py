from drafter.report import PngReport
from drafter.node import Node
from drafter.nodes.text import Text
from drafter.layouts.row import Row
from drafter.nodes.auto_scale import AutoScale
from drafter.utils.pos_size import Justify
from drafter.utils.border import Border


root = Row(
    width='100%',
    height='100%',
    justify=Justify.SPACE_BETWEEN,
    background=[1, 1, 1, 1],
    children=[
        # Node(
        #     width='50%',
        #     height='50%',
        #     background=[1, 0, 0, 1],
        # ),
        AutoScale(
            width='50%',
            height='100%',
            children=[
                Text(
                background=[1, 0, 0, 1],
                    text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',  # noqa
                    width='100%',
                    font_size=16,
                    color='#000',
                    alignment=Text.JUSTIFY,
                    vertical_alignment=Text.MIDDLE,
                ),
            ]
        ),
        Node(
            width='20%',
            height='100%',
            background=[0, 1, 1, 1],
            border=Border(width=10, color=[0, 0, 1, 1])
        )
    ]
)

PngReport('test.png', 256, 256).draw_page(root)
