import pickle

from py2048 import Board
from py2048 import Display

import tornadobase.handlers


class IndexHandler(tornadobase.handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['boards']

    def get(self):
        self.render('index.html')


class TurnHandler(tornadobase.handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['boards']

    async def get(self, boardid=None):
        if boardid:
            board = await self.get_board(boardid)
            if board is None:
                self.send_error(status_code=404,
                                reason='Board state not found')
                return
        else:
            board = Board.new_board()
            await self.save_board(board)

        left = board.shift_left()
        right = board.shift_right()
        up = board.shift_up()
        down = board.shift_down()

        moves = [state
                 for state, score in [left, right, up, down]
                 if score is not None]

        for state in moves:
            await self.save_board(state)

        self.set_header('Content-type', 'application/json')
        self.write({
            'boardid': board.id,
            'moves': [board.id for board in moves]
        })

    async def get_board(self, boardid):
        board = await self.collection.find_one({'boardid': boardid})
        if board is not None:
            state = board.get('state')
            return pickle.loads(state)
        return None

    async def save_board(self, board):
        existing = await self.get_board(board.id)

        if existing is None:
            result = await self.collection.insert({
                'boardid': str(board.id),
                'state': pickle.dumps(board)}, j=True)
            return result

        return None


class ImageHandler(tornadobase.handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['boards']

    def get_current_user(self):
        '''Temporary work-around.  Look for update to tornadobase.'''
        return None

    async def get(self, boardid):
        width = self.get_argument('width', default=200)
        height = self.get_argument('height', default=200)

        board = await self.get_board(boardid)
        if board is None:
            self.send_error(status_code=404, reason='Board not found')
            return

        svg = Display.for_notebook(board, width=width, height=height)

        self.set_header('Content-type', 'image/svg+xml')
        self.set_header('Cache-Control', 'nocache')
        self.write(svg)

    async def get_board(self, boardid):
        board = await self.collection.find_one({'boardid': boardid})
        if board is not None:
            state = board.get('state')
            return pickle.loads(state)
        return None
