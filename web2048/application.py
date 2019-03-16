import tornadobase.application
from tornado.options import define, options

import motor

import handlers


class Application(tornadobase.application.Application):

    def init_handlers(self):
        self.handlers = [
            (r'/image/(.*)', handlers.ImageHandler),
            (r'/turn/(.*)', handlers.TurnHandler),
            (r'/(.*)?', handlers.IndexHandler)
        ]

    def init_options(self):
        define('db_name', help='Name of database.')
        define('db_path', help='Path to mongodb instance.')
        define('static_path', help='Path to static web assets.')

        super().init_options()

    def init_settings(self):
        settings = super().init_settings()
        db_client = motor.MotorClient(options.db_path)
        db_ref = db_client[options.db_name]

        settings.update({
            'db_ref': db_ref,
            'static_path': options.static_path
        })

        return settings


if __name__ == '__main__':
    app = Application()
    app.start()
