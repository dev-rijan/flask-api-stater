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
from src.schemas.default import SuccessSchema
from src.services.user import UserService

create_user_schema = CreateUserSchema()
profile_schema = ProfileSchema()
update_user_schema = UpdateUserSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
update_identity_schema = UpdateIdentitySchema()
update_password_schema = UpdatePasswordSchema()
succsss_schema = SuccessSchema()


class UsersView(BaseView):
    @admin_required
    def index(self):
        """Get all users Resource
        ---
        description: Get all Users
        security:
          - jwt: []
        responses:
          200:
            content:
              application/json:
                schema: UserSchema
        """
        users = UserService.get_all()

        return {
            'users': users_schema.dump(users)
        }

    @admin_required
    def get(self, id):
        """Get single user Resource
        ---
        description: Get User
        security:
          - jwt: []
        parameters:
        - name: "id"
          in: "path"
          description: "id of required user"
          required: true
          type: "int"
        responses:
          200:
            content:
              application/json:
                schema: UserSchema
        """
        user = UserService.get_by_id(id)
        if not user:
            return {'errors': 'user not found'}, 422

        return {
            'user': user_schema.dump(user)
        }

    @admin_required
    def post(self):
        """Create User Resource
        ---
        description: Create User
        security:
          - jwt: []
        requestBody:
          content:
            application/json:
              schema: CreateUserSchema
        responses:
          200:
            content:
              application/json:
                schema: UserSchema
        """
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
        """Update User Resource
        ---
        description: Update User
        security:
          - jwt: []
        parameters:
        - name: "id"
          in: "path"
          description: "id of required user"
          required: true
          type: "int"
        requestBody:
          content:
            application/json:
              schema: UpdateUserSchema
        responses:
          200:
            content:
              application/json:
                schema: UserSchema
        """
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
        """Enable User Resource
        ---
        description: Enable User
        security:
          - jwt: []
        parameters:
        - name: "id"
          in: "path"
          description: "id of user to enable"
          required: true
          type: "int"
        responses:
          200:
            content:
              application/json:
                schema: UserSchema
        """

        user = UserService.enable(id)

        return {
            'user': user_schema.dump(user)
        }

    @route('<id>/disable', methods=['POST'])
    @admin_required
    def disable(self, id):
        """Disable User Resource
        ---
        description: Disable User
        security:
          - jwt: []
        parameters:
        - name: "id"
          in: "path"
          description: "id of user to disable"
          required: true
          type: "int"
        responses:
          200:
            content:
              application/json:
                schema: UserSchema
        """
        user = UserService.disable(id)

        return {
            'user': user_schema.dump(user)
        }

    @route('/update_password', methods=['POST'])
    @auth_required
    def update_password(self):
        """Update Password Resource
        ---
        description: Update Password
        security:
          - jwt: []
        requestBody:
          content:
            application/json:
              schema: UpdatePasswordSchema
        responses:
          200:
            content:
              application/json:
                schema: SuccessSchema
        """
        json_data = request.get_json()
        try:
            data = update_password_schema.load(json_data)
        except ValidationError as error:
            return {'errors': error.messages}, 422

        if not current_user.authenticated(password=data['current_password']):
            return {'errors': 'Current password not matched'}, 422

        UserService.update_password(data['new_password'], current_user)

        response = {
            'success': True,
            'message': 'Successfully updated password'
        }
        return succsss_schema.dump(response)
