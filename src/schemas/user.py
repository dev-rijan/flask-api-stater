from flask_jwt_extended import current_user
from marshmallow import fields, validates_schema, ValidationError

from src.extensions import ma
from src.services.user import UserService

ERROR_MESSAGES = {
    'unique': '{0} Must be unique.',
    'invalid_password': 'Password not matched'
}


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True)
    name_kana = fields.String(required=True)


class UserSchema(ma.Schema):
    id = fields.Integer()
    role = fields.String(required=True)
    email = fields.Email(required=True)
    is_active = fields.Boolean(dump_only=True)
    username = fields.String(required=True)
    profile = ma.Nested(ProfileSchema, required=True)


class CreateUserSchema(UserSchema):
    password = fields.String(required=True)
    id = fields.Integer(dump_only=True)

    @validates_schema
    def validate_email(self, data, **kwargs):
        if UserService.find_by_identity(data['email']):
            raise ValidationError({
                'email': ERROR_MESSAGES['unique'].format('Email')
            })

    @validates_schema
    def validate_username(self, data, **kwargs):
        if UserService.find_by_identity(data['username']):
            raise ValidationError({
                'username': ERROR_MESSAGES['unique'].format('Username')
            })


class UpdateUserSchema(UserSchema):
    id = fields.Integer(required=True)

    @validates_schema
    def validate_email(self, data, **kwargs):
        user = UserService.find_by_identity(data['email'])

        if user and user.id != data['id']:
            raise ValidationError({
                'email': ERROR_MESSAGES['unique'].format('Email')
            })

    @validates_schema
    def validate_username(self, data, **kwargs):
        user = UserService.find_by_identity(data['username'])

        if user and user.id != data['id']:
            raise ValidationError({
                'username': ERROR_MESSAGES['unique'].format('Username')
            })


class UpdatePasswordSchema(ma.Schema):
    current_password = fields.String(required=True)
    new_password = fields.String(required=True)

    @validates_schema
    def validate_current_password(self, data, **kwargs):
        if not current_user.authenticated(password=data['current_password']):
            raise ValidationError({
                'current_password': ERROR_MESSAGES['invalid_password']
            })
