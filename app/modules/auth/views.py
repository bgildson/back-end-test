# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from app.utils.db import db
from .models import User
from .schemas import RegisterSchema, LoginSchema


bp = Blueprint('auth', __name__, url_prefix='/api/auth')
register_schema = RegisterSchema()
login_schema = LoginSchema()


@bp.route('/register', methods=['POST'])
def register():
    """
    Handle requests to register a new user
    """
    try:
        data = request.get_json()

        errors = register_schema.validate(data)
        if errors:
            return jsonify(errors=errors), 400

        user = User.get_by_username(data['username'])
        if user:
            msg = f'Just exists an user with "{user.username}" username'
            return jsonify({'error': msg}), 409

        user = User(**data)
        db.session.add(user)
        db.session.commit()

        return jsonify(access_token=create_access_token(user)), 200
    except Exception:
        db.session.rollback()
        return (
            jsonify(
                error='An unexpected error has occurred, please try again in a few minutes'
            ),
            500,
        )


@bp.route('/login', methods=['POST'])
def login():
    """
    Handle requests to make login
    """
    try:
        data = request.get_json()

        errors = login_schema.validate(data)
        if errors:
            return jsonify(errors=errors), 400

        user = User.get_by_username_and_password(data['username'], data['password'])
        if not user:
            return jsonify(error='Invalid Username or Password'), 401

        return jsonify(access_token=create_access_token(user)), 200
    except Exception:
        return (
            jsonify(
                error='An unexpected error has occurred, please try again in a few minutes'
            ),
            500,
        )
