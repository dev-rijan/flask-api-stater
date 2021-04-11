from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
ma = Marshmallow()
jwt = JWTManager()
