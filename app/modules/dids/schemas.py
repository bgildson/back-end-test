# -*- coding: utf-8 -*-

from decimal import ROUND_DOWN

from marshmallow import Schema, fields, validate, EXCLUDE


class DIDSchema(Schema):
    """
    Represents and handles a did interaction through api
    """

    class Meta:
        unknown = EXCLUDE

    id = fields.UUID(dump_only=True)
    value = fields.String(
        required=True,
        allow_none=False,
        validate=validate.Length(min=3, max=20),
    )
    monthy_price = fields.Decimal(
        data_key='monthyPrice',
        required=True,
        allow_none=False,
        allow_nan=False,
        as_string=True,
        validate=validate.Range(min=0, min_inclusive=True),
        places=2,
        rounding=ROUND_DOWN,
    )
    setup_price = fields.Decimal(
        data_key='setupPrice',
        required=True,
        allow_none=False,
        allow_nan=False,
        as_string=True,
        validate=validate.Range(min=0, min_inclusive=True),
        places=2,
        rounding=ROUND_DOWN,
    )
    currency = fields.String(
        required=True,
        allow_none=False,
        validate=validate.Length(min=1, max=3),
    )
