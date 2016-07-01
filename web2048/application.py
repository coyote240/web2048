import tornadobase.application

import handlers


class Application(tornadobase.application.Application):

    def init_handlers(self):
        self.handlers = [
            (r'/', handlers.IndexHandler),
            (r'/image/(.*)', handlers.ImageHandler)
        ]


if __name__ == '__main__':
    app = Application()
    app.start()
