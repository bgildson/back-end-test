# -*- coding: utf-8 -*-

from flask import Flask
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
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
def client(app: Flask):
    """
    Creates a http client injectable in session level
    """
    return app.test_client()


@pytest.fixture(scope='session')
def aclient(app: Flask, access_token: str):
    """
    Creates an authenticated http client injectable in session level
    """
    client = app.test_client()
    client.environ_base['HTTP_AUTHORIZATION'] = f'JWT {access_token}'
    return client


@pytest.fixture(scope='session', autouse=True)
def db(app: Flask):
    """
    Creates the tests db injectable in session level
    """
    with app.app_context():
        _db.create_all()

        yield _db

        _db.drop_all()


@pytest.fixture(scope='session')
def user(db: SQLAlchemy):
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


@pytest.fixture(scope='session')
def access_token(app: Flask, user: User):
    with app.test_request_context():
        u = User.get_by_username(user['username'])
        return create_access_token(u)
