# -*- coding: utf-8 -*-

from flask import Flask

from .views import bp


def init_app(app: Flask):
    app.register_blueprint(bp)
