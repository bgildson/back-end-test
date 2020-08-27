# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.utils.db import db
from .models import DID
from .schemas import DIDSchema


bp = Blueprint('dids', __name__, url_prefix='/dids')
did_schema = DIDSchema()


@bp.route('/<string:pk>')
@jwt_required
def get_one(pk: str):
    """
    Find one did based in the pk
    """
    try:
        did = DID.get_by_id(pk)
        if not did:
            return jsonify(error=f'The DID with id "{pk}" was not found'), 404

        data = did_schema.dump(did)

        return jsonify(data), 200
    except Exception:
        return (
            jsonify(
                error='An unexpected error has occurred, please try again in a few minutes'
            ),
            500,
        )


@bp.route('/')
@jwt_required
def get_many():
    """
    Find many did's ordered by the ordest
    """
    try:
        start = 0
        size = 20

        if 'start' in request.args:
            _start = request.args['start']
            if not _start.isdigit():
                return (
                    jsonify(error='The start argument must be a positive digit'),
                    400,
                )
            start = int(_start)

        if 'size' in request.args:
            _size = request.args['size']
            if not _size.isdigit():
                return (
                    jsonify(error='The size argument must be a positive digit'),
                    400,
                )
            size = int(_size)

        dids = DID.get_by_start_and_size(start, size)
        data = did_schema.dump(dids, many=True)

        return jsonify(data), 200
    except Exception:
        return (
            jsonify(
                error='An unexpected error has occurred, please try again in a few minutes'
            ),
            500,
        )


@bp.route('/', methods=['POST'])
@jwt_required
def create():
    """
    Creates a new did
    """
    try:
        errors = did_schema.validate(request.get_json())
        if errors:
            return jsonify(errors=errors), 400

        data = did_schema.load(request.get_json())

        did = DID.get_by_value(data['value'])
        if did:
            return (
                jsonify(error=f'There is already a DID with the value "{did.value}"'),
                409,
            )

        did = DID(**data)
        db.session.add(did)
        db.session.commit()

        result = did_schema.dump(did)

        return jsonify(result), 201
    except Exception:
        db.session.rollback()
        return (
            jsonify(
                error='An unexpected error has occurred, please try again in a few minutes'
            ),
            500,
        )


@bp.route('/<string:pk>', methods=['PUT'])
@jwt_required
def update(pk: str):
    """
    Update an existing did
    """
    try:
        did = DID.get_by_id(pk)
        if not did:
            return jsonify(error=f'The DID with id "{pk}" was not found'), 404

        errors = did_schema.validate(request.get_json())
        if errors:
            return jsonify(errors=errors), 400

        data = did_schema.load(request.get_json())

        other = DID.get_by_value(data['value'])
        if other and str(other.id) != pk:
            return (
                jsonify(error=f'There is already a DID with the value "{other.value}"'),
                409,
            )

        for key, value in data.items():
            setattr(did, key, value)
        db.session.commit()

        result = did_schema.dump(did)

        return jsonify(result), 200
    except Exception:
        db.session.rollback()
        return (
            jsonify(
                error='An unexpected error has occurred, please try again in a few minutes'
            ),
            500,
        )


@bp.route('/<string:pk>', methods=['DELETE'])
@jwt_required
def remove(pk: str):
    """
    Remove an existing did
    """
    try:
        did = DID.get_by_id(pk)
        if not did:
            return jsonify(error=f'The DID with id "{pk}" was not found'), 404

        db.session.delete(did)
        db.session.commit()

        return jsonify(''), 204
    except Exception:
        return (
            jsonify(
                error='An unexpected error has occurred, please try again in a few minutes'
            ),
            500,
        )
