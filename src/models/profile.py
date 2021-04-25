from src.mixins.resource import ResourceMixin
from src.extensions import db


class Profile(db.Model, ResourceMixin):
    __tablename__ = 'profiles'

    id = db.Column(
        db.Integer,
        db.ForeignKey(
            'users.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        primary_key=True
    )
    name = db.Column(db.String(120), nullable=False)
    name_kana = db.Column(db.String(120))
