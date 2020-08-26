# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class RegisterSchema(Schema):
    """
    Represents which is the expected payload when registering
    """

    username = fields.String(required=True)
    password = fields.String(required=True)


class LoginSchema(Schema):
    """
    Represents which is the expected payload when login
    """

    username = fields.String(required=True)
    password = fields.String(required=True)
