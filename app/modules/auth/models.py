# -*- coding: utf-8 -*-

from __future__ import annotations
from datetime import datetime
import uuid
from sqlalchemy_utils import types
from werkzeug.security import generate_password_hash, check_password_hash

from app.utils.db import db


class User(db.Model):
    """
    Represents an app user
    """

    __tablename__ = 'users'

    id = db.Column(types.UUIDType(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username=None, password=None):
        """
        Implements the constructor to set password properly
        """
        self.username = username
        self.set_password(password)

    @classmethod
    def get_by_username(self, username) -> User:
        """
        Get an user with an username equals to the username parameter
        """
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_by_username_and_password(self, username, password) -> User:
        """
        Get an user that matches the username and the password
        """
        user = User.get_by_username(username)
        if user and user.check_password(password):
            return user
        return None

    def set_password(self, password):
        """
        Takes the password and make the properly hash operation before set it
        """
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """
        Takes the password and verify if the password matches with the user password
        """
        return check_password_hash(self.password, password)
