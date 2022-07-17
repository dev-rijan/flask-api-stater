from flask import request
from flask_classful import route
from flask_jwt_extended import current_user
from webargs.flaskparser import parser

from src.decorators.acl_decorators import admin_required, auth_required
from src.resources.base import BaseView
from src.schemas.user import (
    CreateUserSchema,
    UserSchema,
    UpdateUserSchema,
    UpdatePasswordSchema,
)
from src.services.user import UserService

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UsersView(BaseView):
    @admin_required
    def index(self):
        """Get all users Resource
        ---
        tags:
          - users
        description: Get all Users
        security:
          - jwt: []
        responses:
          200:
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    users:
                        type: array
                        items: UserSchema
        """
        users = UserService.get_all()

        return {
            'users': users_schema.dump(users)
        }

    @admin_required
    def get(self, id):
        """Get single user Resource
        ---
        tags:
          - users
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
                schema:
                  type: object
                  properties:
                    user: UserSchema
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
        tags:
          - users
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
                schema:
                  type: object
                  properties:
                    user: UserSchema
        """

        data = parser.parse(CreateUserSchema, request)
        user = UserService.create(data)

        return {
            'user': user_schema.dump(user)
        }

    @admin_required
    def put(self, id):
        """Update User Resource
        ---
        tags:
          - users
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
                schema:
                  type: object
                  properties:
                    user: UserSchema
        """
        data = parser.parse(UpdateUserSchema, request)
        user = UserService.update(id, data)

        return {
            'user': user_schema.dump(user)
        }

    @route('<id>/enable', methods=['POST'])
    @admin_required
    def enable(self, id):
        """Enable User Resource
        ---
        tags:
          - users
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
                schema:
                  type: object
                  properties:
                    user: UserSchema
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
        tags:
          - users
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
                schema:
                  type: object
                  properties:
                    user: UserSchema
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
        tags:
          - users
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
                schema:
                  type: object
                  properties:
                    success:
                      type: Boolean
                      example: True
                    message:
                      type: String
                      example: String
        """
        data = parser.parse(UpdatePasswordSchema, request)
        UserService.update_password(data['new_password'], current_user)

        return {
            'success': True,
            'message': 'Successfully updated password'
        }
