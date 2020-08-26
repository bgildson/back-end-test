# -*- coding: utf-8 -*-

from flask import Flask

from .utils.jwt import jwt
from .views import bp


def init_app(app: Flask):
    jwt.init_app(app)
    app.register_blueprint(bp)
