from marshmallow import fields
from src.extensions import ma


class SuccessSchema(ma.Schema):
    code = fields.Integer(required=True)
    message = fields.String(required=True)
