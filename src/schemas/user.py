from marshmallow import fields, validates_schema, ValidationError

from src.extensions import ma
from src.models.profile import Profile
from src.services.user import UserService


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'name_kana')


class UserSchema(ma.Schema):
    id = fields.Integer()
    role = fields.String(required=True)
    email = fields.Email(required=True)
    is_active = fields.Boolean(dump_only=True)
    username = fields.String(required=True)
    profile = ma.Nested(ProfileSchema, required=True)


class CreateUserSchema(UserSchema):
    password = fields.String(required=True)

    @validates_schema
    def validate_email(self, data, **kwargs):
        if UserService.find_by_identity(data['email']):
            raise ValidationError('Email must be unique.')

    @validates_schema
    def validate_username(self, data, **kwargs):
        if UserService.find_by_identity(data['username']):
            raise ValidationError('Username must be unique.')


class UpdateUserSchema(UserSchema):
    id = fields.Integer(required=True)

    @validates_schema
    def validate_email(self, data, **kwargs):
        user = UserService.find_by_identity(data['email'])

        if user and user.id != data['id']:
            raise ValidationError('Email must be unique.')

    @validates_schema
    def validate_username(self, data, **kwargs):
        user = UserService.find_by_identity(data['username'])

        if user and user.id != data['id']:
            raise ValidationError('Username must be unique.')


class UpdateIdentitySchema(ma.Schema):
    id = fields.Integer()
    email = fields.String(required=True)
    username = fields.String(required=True)

    @validates_schema
    def validate_email(self, data, **kwargs):
        user = UserService.find_by_identity(data['email'])

        if user and user.id != data['id']:
            raise ValidationError('Email must be unique.')

    @validates_schema
    def validate_username(self, data, **kwargs):
        user = UserService.find_by_identity(data['username'])

        if user and user.id != data['id']:
            raise ValidationError('Username must be unique.')


class UpdatePasswordSchema(ma.Schema):
    current_password = fields.String(required=True)
    new_password = fields.String(required=True)
