from flask import Flask
from flask_cors import CORS
from werkzeug.debug import DebuggedApplication

from src.models.revoked_token import RevokedToken
from src.models.user import User
from src.resources.default_view import DefaultView
from src.resources.auth import AuthView
from src.resources.user import UsersView
from cli import register_cli_commands

from src.extensions import debug_toolbar, flask_static_digest, db, migrate, ma, jwt, mail


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, static_folder='../public', static_url_path='')

    app.config.from_object('config.settings')

    if settings_override:
        app.config.update(settings_override)

    # initialize cors
    CORS(app, supports_credentials=True, allow_headers="*", resources={
        r"/*": {
            "origins": "*"
        }})

    app.config['CORS_HEADERS'] = 'Content-Type'

    extensions(app)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    UsersView.register(app, trailing_slash=False)
    AuthView.register(app)
    DefaultView.register(app, trailing_slash=False)

    register_cli_commands(app)

    jwt_callbacks(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    db.init_app(app)
    flask_static_digest.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app=app, db=db)
    mail.init_app(app)

    return None


def jwt_callbacks(app, user_model):
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.email

    @jwt.additional_claims_loader
    def add_claims_to_access_token(user):
        return {'role': user.role}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return RevokedToken.is_jti_blacklisted(jti)

    @jwt.user_lookup_loader
    def user_loader_callback(jwt_header, jwt_data):
        identity = jwt_data['sub']
        return user_model.find_by_identity(identity)
