# -*- coding: utf-8 -*-

from flask.helpers import url_for
import pytest


@pytest.fixture(scope='session')
def auth_register_url(app):
    """
    URL used to access the auth resource register action
    """
    with app.test_request_context():
        return url_for('auth.register')


@pytest.fixture(scope='session')
def auth_login_url(app):
    """
    URL used to access the auth resource login action
    """
    with app.test_request_context():
        return url_for('auth.login')
