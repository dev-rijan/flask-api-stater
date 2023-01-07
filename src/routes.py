from src.resources.auth import AuthView
from src.resources.user import UsersView
from src.resources.docs import DocsView
from src.resources.default_view import DefaultView
from src.extensions import apispec


def register(app):
    # Register routes
    UsersView.register(app, trailing_slash=False)
    AuthView.register(app, trailing_slash=False)
    DocsView.register(app, trailing_slash=False)
    DefaultView.register(app, trailing_slash=False)

    # Register docs
    apispec.paths(AuthView)
    apispec.paths(UsersView)

    jwt_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    apispec.components.security_scheme("jwt", jwt_scheme)
