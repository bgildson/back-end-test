# -*- coding: utf-8 -*-

from flask_jwt_extended import JWTManager

from ..models import User


jwt: JWTManager = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    Specifies which field will be used to identify the jwt subject
    """
    return user.id


@jwt.user_loader_callback_loader
def user_loader(identity):
    """
    Receives the jwt subject and returns the owner
    """
    return User.query.filter_by(id=identity).first()
