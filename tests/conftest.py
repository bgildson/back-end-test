# -*- coding: utf-8 -*-

import pytest

from app import create_app
from app.modules.auth.models import User
from app.utils.db import db as _db


@pytest.fixture(scope='session')
def app():
    """
    Creates an app injectable in session level
    """
    return create_app('testing')


@pytest.fixture(scope='session')
def client(app):
    """
    Creates a http client injectable in session level
    """
    return app.test_client()


@pytest.fixture(scope='session', autouse=True)
def db(app):
    """
    Creates the tests db injectable in session level
    """
    with app.app_context():
        _db.create_all()

        yield _db

        _db.drop_all()


@pytest.fixture(scope='session')
def user(db):
    """
    Creates an user that could be used in the tests
    """
    password = '123456'
    user = User(username='myusername', password=password)
    db.session.add(user)
    db.session.commit()

    return {
        'id': user.id,
        'username': user.username,
        'password': password,
    }
