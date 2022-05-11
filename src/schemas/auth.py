from marshmallow import fields

from src.extensions import ma
from src.schemas.user import UserSchema


class LoginSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class LoginResponseSchema(ma.Schema):
    access_token = fields.String()
    refresh_token = fields.String()
    user = ma.Nested(UserSchema)


class ResetPasswordSchema(ma.Schema):
    password = fields.String(required=True)


class ResetPasswordRequestSchema(ma.Schema):
    email = fields.Email(required=True)


class SignUpSchema(LoginSchema):
    pass
