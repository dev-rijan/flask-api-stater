from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_classful_apispec import APISpec

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
ma = Marshmallow()
jwt = JWTManager()
apispec = APISpec()
