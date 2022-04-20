from collections import OrderedDict
from hashlib import md5

from flask import current_app
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import expression

from itsdangerous import URLSafeTimedSerializer

from src.mixins.resource import ResourceMixin
from src.extensions import db
from src.models.profile import Profile


class User(ResourceMixin, db.Model):
    ROLE_ADMIN = 'ROLE_ADMIN'
    ROLE_USER = 'ROLE_USER'

    ROLES = OrderedDict([
        (ROLE_ADMIN, 'ROLE_ADMIN'),
        (ROLE_USER, 'ROLE_USER')
    ])

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # Authentication.
    role = db.Column(db.Enum(*ROLES, name='role_types', native_enum=False),
                     nullable=False, default=ROLE_ADMIN)
    is_active = db.Column('is_active', db.Boolean(), nullable=False,
                          server_default=expression.true())
    username = db.Column(db.String(24), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    profile = db.relationship(
        Profile,
        backref='user',
        lazy=True,
        uselist=False
    )

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(User, self).__init__(**kwargs)

        self.password = User.encrypt_password(kwargs.get('password', ''))

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a user by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        return User.query.filter(
            (User.email == identity) | (User.username == identity)).first()

    @classmethod
    def encrypt_password(cls, plaintext_password):
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            return generate_password_hash(plaintext_password)

        return None

    @classmethod
    def deserialize_token(cls, token):
        """
        Obtain a user from de-serializing a signed token.

        :param token: Signed token.
        :type token: str
        :return: User instance or None
        """
        pass
        # private_key = TimedJSONWebSignatureSerializer(
        #     current_app.config['SECRET_KEY'])
        # try:
        #     decoded_payload = private_key.loads(token)

        #     return User.find_by_identity(decoded_payload.get('user_email'))
        # except Exception:
        #     return None

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (User.email.ilike(search_query),
                        User.username.ilike(search_query))

        return or_(*search_chain)

    @classmethod
    def is_last_admin(cls, user, new_role, new_active):
        """
        Determine whether or not this user is the last admin account.

        :param user: User being tested
        :type user: User
        :param new_role: New role being set
        :type new_role: str
        :param new_active: New active status being set
        :type new_active: bool
        :return: bool
        """
        is_changing_roles = user.role == 'admin' and new_role != 'admin'
        is_changing_active = user.active is True and new_active is None

        if is_changing_roles or is_changing_active:
            admin_count = User.query.filter(User.role == 'admin').count()
            active_count = User.query.filter(User.is_active is True).count()

            if admin_count == 1 or active_count == 1:
                return True

        return False

    def get_auth_token(self):
        """
        Return the user's auth token. Use their password as part of the token
        because if the user changes their password we will want to invalidate
        all of their logins across devices. It is completely fine to use
        md5 here as nothing leaks.

        This satisfies Flask-Login by providing a means to create a token.

        :return: str
        """
        private_key = current_app.config['SECRET_KEY']

        serializer = URLSafeTimedSerializer(private_key)
        data = [str(self.id), md5(self.password.encode('utf-8')).hexdigest()]

        return serializer.dumps(data)

    def authenticated(self, with_password=True, password=''):
        """
        Ensure a user is authenticated, and optionally check their password.

        :param with_password: Optionally check their password
        :type with_password: bool
        :param password: Optionally verify this as their password
        :type password: str
        :return: bool
        """
        if with_password:
            return check_password_hash(self.password, password)

        return True

    def serialize_token(self, expiration=3600):
        """
        Sign and create a token that can be used for things such as resetting
        a password or other tasks that involve a one off token.

        :param expiration: Seconds until it expires, defaults to 1 hour
        :type expiration: int
        :return: JSON
        """
        pass
        # private_key = current_app.config['SECRET_KEY']

        # serializer = TimedJSONWebSignatureSerializer(private_key, expiration)
        # return serializer.dumps({'user_email': self.email}).decode('utf-8')

    def is_admin(self):
        """
        Return whether or not the user is admin

        :return: bool
        """
        return True if self.role == self.ROLE_ADMIN else False

    def is_client(self):
        """
        Return whether or not the user is client

        :return: bool
        """
        return True if self.role == self.ROLE_CLIENT else False

    def is_iot(self):
        """
        Return whether or not the user is iot

        :return: bool
        """
        return True if self.role == self.ROLE_IOT else False
