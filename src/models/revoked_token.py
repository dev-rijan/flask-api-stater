from src.extensions import db
from src.mixins.resource import ResourceMixin


class RevokedToken(db.Model, ResourceMixin):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), unique=True, nullable=False)

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """
        Check whether given token is blacklisted or not

        :param jti: Unique identifier of jwt token
        :type jti: str
        :return: boolean
        """
        token = cls.query.filter_by(jti=jti).first()
        return bool(token)
