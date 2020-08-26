# -*- coding: utf-8 -*-

from . import auth


def init_app(app):
    auth.init_app(app)
