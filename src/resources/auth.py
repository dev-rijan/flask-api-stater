from flask_classful import route
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity,
                                get_jwt)

from src.resources.base import BaseView
from src.schemas.auth import LoginSchema, RefreshTokenSchema
from src.services.authentication_manager import AuthenticationManager
from src.decorators.request_parser import use_args_with

authentication_manager = AuthenticationManager()


class AuthView(BaseView):
    @route('/login', methods=['POST'])
    @use_args_with(LoginSchema)
    def login(self, data):
        """Login Resource
        ---
        description: Login with username/email and password
        tags:
          - auth
        security:
          - jwt: []
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
        return authentication_manager.login(data)

    @route('/access/revoke', methods=['DELETE'])
    @jwt_required()
    def access_token_revoke(self):
        """Get an access token from a refresh token
          ---
          tags:
            - auth
          security:
          - jwt: []
          summary: Revoke an access token
          description: Revoke an access token
          responses:
            200:
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                        example: access token has been revoked
            400:
              description: bad request
            401:
              description: unauthorized
        """
        jti = get_jwt()['jti']

        try:
            authentication_manager.revoke_token(jti)

            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

    @route('/refresh/revoke', methods=['DELETE'])
    @jwt_required(refresh=True)
    def refresh_token_revoke(self):
        """Get an access token from a refresh token
          ---
          tags:
            - auth
          security:
          - jwt: []
          summary: Revoke an refresh token
          description: Revoke an refresh token
          responses:
            200:
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                        example: refresh token has been revoked
            400:
              description: bad request
            401:
              description: unauthorized
        """
        jti = get_jwt()['jti']

        try:
            authentication_manager.revoke_token(jti)

            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

    @route('/refresh_token', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh_token(self):
        """Get an access token from a refresh token
          ---
          tags:
            - auth
          security:
          - jwt: []
          summary: Get an access token
          description: Get an access token by using a refresh token in the `Authorization` header
          responses:
            200:
              content:
                application/json:
                  schema: RefreshTokenSchema
            400:
              description: bad request
            401:
              description: unauthorized
        """
        current_user = get_jwt_identity()
        tokens = authentication_manager.refresh_token(identity=current_user)

        return RefreshTokenSchema().dump(tokens)
  # @route('/reset_password_request', methods=['POST'])
    # def reset_password_request(self):
    #     # [TODO: RA] Impliment reset password feature
    #     pass

    # @route('/reset_password/<token>', methods=['POST'])
    # def reset_password(self, token):
    #     # [TODO: RA] Impliment reset password feature
    #     pass
