from py2048 import Board
from py2048 import Display

import tornadobase.handlers


class IndexHandler(tornadobase.handlers.BaseHandler):

    def get(self):
        self.write('foo')


class ImageHandler(tornadobase.handlers.BaseHandler):

    def get(self, id):
        board = Board()
        svg = Display.for_notebook(board)

        self.set_header('Content-type', 'image/svg+xml')
        self.write(svg)
