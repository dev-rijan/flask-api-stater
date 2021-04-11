from marshmallow import fields

from src.extensions import ma


class LoginSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class ResetPasswordSchema(ma.Schema):
    password = fields.String(required=True)


class ResetPasswordRequestSchema(ma.Schema):
    identity = fields.String(required=True)


class SignUpSchema(LoginSchema):
    pass
