from marshmallow import fields

from src.extensions import ma


class LoginSchema(ma.Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class LoginResponseSchema(ma.Schema):
    access_token = fields.String()
    refresh_token = fields.String()
    expired_at = fields.Integer()


class RefreshTokenSchema(ma.Schema):
    access_token = fields.String()
    refresh_token = fields.String()
    expires_in = fields.Integer()


class ResetPasswordSchema(ma.Schema):
    password = fields.String(required=True)


class ResetPasswordRequestSchema(ma.Schema):
    email = fields.Email(required=True)


class SignUpSchema(LoginSchema):
    pass
