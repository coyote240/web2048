import pickle
import random

from py2048 import Board as OldBoard
from py2048 import Display

import tornadobase.handlers


class Board(OldBoard):

    def add_random_cell(self):
        '''Return a new board with the addition of one random cell.
        '''
        board = Board(self)
        coords = board.get_empty_cells()
        selected = random.choice(coords)
        board[selected] = random.randint(1, 2) * 2
        return board

    def shift_left(self):
        board, score = super().shift_left()
        board = board.add_random_cell()
        board = board.add_random_cell()
        return board, score

    def shift_right(self):
        board, score = super().shift_right()
        board = board.add_random_cell()
        board = board.add_random_cell()
        return board, score

    def shift_up(self):
        board, score = super().shift_up()
        board = board.add_random_cell()
        board = board.add_random_cell()
        return board, score

    def shift_down(self):
        board, score = super().shift_down()
        board = board.add_random_cell()
        board = board.add_random_cell()
        return board, score


class IndexHandler(tornadobase.handlers.BaseHandler):

    def prepare(self):
        self.collection = self.settings['db_ref']['boards']

    def get(self, boardid=''):
        self.render('index.html', boardid=boardid)


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

        moves = [(state, score)
                 for state, score in [left, right, up, down]
                 if score is not None]

        for state, score in moves:
            await self.save_board(state)

        self.set_header('Content-type', 'application/json')
        self.write({
            'boardid': str(board.id),
            'moves': [{
                'id': str(board.id),
                'score': score
            } for board, score in moves]
        })

    async def get_board(self, boardid):
        board = await self.collection.find_one({'boardid': boardid})
        if board is not None:
            state = board.get('state')
            return pickle.loads(state)
        return None

    async def save_board(self, board):
        result = await self.collection.save({
            'boardid': str(board.id),
            'state': pickle.dumps(board)})
        return result


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
