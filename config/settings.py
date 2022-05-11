import os
from distutils.util import strtobool

from dotenv import load_dotenv

# Load env var from dotenv file
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
env_path = os.path.join(APP_ROOT, '.env')
load_dotenv(env_path)

DEBUG = True

FLASK_APP_VERSION = os.getenv('FLASK_APP_VERSION')

SECRET_KEY = os.getenv('SECRET_KEY')
SERVER_NAME = os.getenv('SERVER_NAME', 'localhost:8000')

# Flask-Mail.
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_USE_TLS = bool(strtobool(os.getenv('MAIL_USE_TLS', 'true')))
MAIL_USE_SSL = bool(strtobool(os.getenv('MAIL_USE_SSL', 'false')))
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

MONITORING_APP_URL = os.getenv('MONITORING_APP_URL')

# SQLAlchemy.
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', '')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SEED_ADMIN_EMAIL = os.getenv('SEED_ADMIN_EMAIL')
SEED_ADMIN_USERNAME = os.getenv('SEED_ADMIN_USERNAME')
SEED_ADMIN_PASSWORD = os.getenv('SEED_ADMIN_PASSWORD')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
ACCESS_TOKEN_EXPIRES_IN = int(os.getenv('ACCESS_TOKEN_EXPIRES_IN', 10))  # in minutes
REFRESH_TOKEN_EXPIRES_IN = int(os.getenv('REFRESH_TOKEN_EXPIRES_IN', 5)) # in days

#Apispec config
DOC_TITLE = os.getenv('DOC_TITLE')
DOC_VERSION = os.getenv('DOC_VERSION')
DOC_OPEN_API_VERSION = os.getenv('DOC_OPEN_API_VERSION', '3.0.2')

TIMEZONE = os.getenv('TIMEZONE', 'Asia/Tokyo')
