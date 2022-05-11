from flask import request, current_app
from flask_classful import route
from marshmallow import ValidationError

from src.resources.base import BaseView
from src.schemas.auth import LoginSchema, ResetPasswordRequestSchema, ResetPasswordSchema
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity,
                                get_jwt)

from src.services.authentication_manager import AuthenticationManager

login_schema = LoginSchema()
reset_password_schema = ResetPasswordSchema()
reset_password_request_schema = ResetPasswordRequestSchema()
authentication_manager = AuthenticationManager()


class AuthView(BaseView):
    @route('/login', methods=['POST'])
    def login(self):
        """Login Resource
        ---
        description: Login with username/email and password
        requestBody:
          content:
            application/json:
              schema: LoginSchema
        responses:
          200:
            content:
              application/json:
                schema: LoginResponseSchema
        """

        json_data = request.get_json()

        try:
            data = login_schema.load(json_data)
        except ValidationError as error:
            return {'errors': error.messages}, 422

        return authentication_manager.login(data)

    @route('/reset_password_request', methods=['POST'])
    def reset_password_request(self):
        json_data = request.get_json()

        try:
            data = reset_password_request_schema.load(json_data)

        except ValidationError as error:
            return {'errors': error.messages}, 422

        user = authentication_manager.find_by_identity(data['identity'])

        if not user:
            return {'message': "Can\'t find username or email"}, 422

        authentication_manager.initialize_password_reset(user)

        return {
            'success': True,
            'message': 'Successfully sent password reset mail'
        }

    @route('/reset_password/<token>', methods=['POST'])
    def reset_password(self, token):
        json_data = request.get_json()

        try:
            data = reset_password_schema.load(json_data)
        except ValidationError as error:
            return {'errors': error.messages}, 422

        user = authentication_manager.deserialize_token(token)

        if not user:
            return {'errors': 'Your reset token has expired or was tampered with.'}, 403

        authentication_manager.reset_password(user, data['password'])

        return {
            'success': True,
            'message': 'Successfully reset password'
        }

    @route('/access/revoke', methods=['POST'])
    @jwt_required()
    def access_token_revoke(self):
        jti = get_jwt()['jti']

        try:
            authentication_manager.revoke_token(jti)

            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

    @route('/refresh/revoke', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh_token_revoke(self):
        jti = get_jwt()['jti']

        try:
            authentication_manager.revoke_token(jti)

            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

    @route('/refresh_token', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh_token(self):
        current_user = get_jwt_identity()

        return authentication_manager.refresh_token(identity=current_user)
