# -*- coding: utf-8 -*-

from . import auth
from . import dids


def init_app(app):
    auth.init_app(app)
    dids.init_app(app)
