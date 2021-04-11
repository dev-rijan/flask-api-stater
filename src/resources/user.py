from flask import request
from flask_classful import route
from flask_jwt_extended import current_user
from marshmallow import ValidationError

from src.decorators.acl_decorators import admin_required, auth_required
from src.resources.base import BaseView
from src.schemas.user import (
    CreateUserSchema,
    UserSchema,
    UpdateUserSchema,
    UpdateIdentitySchema,
    UpdatePasswordSchema,
    ProfileSchema
)
from src.services.user import UserService

create_user_schema = CreateUserSchema()
profile_schema = ProfileSchema()
update_user_schema = UpdateUserSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
update_identity_schema = UpdateIdentitySchema()
update_password_schema = UpdatePasswordSchema()


class UsersView(BaseView):
    @admin_required
    def index(self):
        users = UserService.get_all()

        return {
            'users': users_schema.dump(users)
        }

    @admin_required
    def get(self, id):
        user = UserService.get_by_id(id)
        if not user:
            return {'errors': 'user not found'}, 422

        return {
            'user': user_schema.dump(user)
        }

    @admin_required
    def post(self):
        json_data = request.get_json()
        try:
            data = create_user_schema.load(json_data)
        except ValidationError as error:
            return {'errors': error.messages}, 422

        user = UserService.create(data)

        return {
            'user': user_schema.dump(user)
        }

    @admin_required
    def put(self, id):
        json_data = request.get_json()
        try:
            data = update_user_schema.load(json_data)
        except ValidationError as error:
            return {'errors': error.messages}, 422

        user = UserService.update(id, data)

        return {
            'user': user_schema.dump(user)
        }

    @route('<id>/enable', methods=['POST'])
    @admin_required
    def enable(self, id):
        user = UserService.enable(id)

        return {
            'user': user_schema.dump(user)
        }

    @route('<id>/disable', methods=['POST'])
    @admin_required
    def disable(self, id):
        user = UserService.disable(id)

        return {
            'user': user_schema.dump(user)
        }

    @route('/update_identity', methods=['POST'])
    @auth_required
    def update_identity(self):
        json_data = request.get_json()
        try:
            data = update_identity_schema.load(json_data)
        except ValidationError as error:
            return {'errors': error.messages}, 422

        user = UserService.update_identity(data, current_user)

        return {
            'user': user_schema.dump(user)
        }

    @route('/update_password', methods=['POST'])
    @auth_required
    def update_password(self):
        json_data = request.get_json()
        try:
            data = update_password_schema.load(json_data)
        except ValidationError as error:
            return {'errors': error.messages}, 422

        if not current_user.authenticated(password=data['current_password']):
            return {'errors': 'Current password not matched'}, 422

        UserService.update_password(data['new_password'], current_user)

        return {
            'success': True,
            'message': 'Successfully updated password'
        }

    @route('/update_profile', methods=['POST'])
    @auth_required
    def update_profile(self):
        json_data = request.get_json()
        try:
            data = profile_schema.load(json_data)
        except ValidationError as error:
            return {'errors': error.messages}, 422

        profile = UserService.update_profile(data, current_user)

        return {
            'profile': profile_schema.dump(profile)
        }
