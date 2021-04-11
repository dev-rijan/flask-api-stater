from src.models.profile import Profile
from src.models.user import User


class UserService:
    @staticmethod
    def create(data: dict):
        profile_data = data['profile']
        data.pop('profile')

        user = User(**data)
        profile = Profile(**profile_data, user=user)

        user.save()
        profile.save()

        return user

    @classmethod
    def enable(cls, id: int):
        user = cls.get_by_id(id)
        user.is_active = True
        user.save()

        return user

    @classmethod
    def disable(cls, id: int):
        user = cls.get_by_id(id)
        user.is_active = False
        user.save()

        return user

    @staticmethod
    def find_by_identity(value):
        return User.find_by_identity(value)

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_all_customers(include_disabled=False):
        query = User.query.filter(User.role == User.ROLE_CLIENT)

        if not include_disabled:
            query = query.filter(User.is_active.is_(True))

        return query.all()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def update(id, data):
        profile_data = data['profile']
        data.pop('profile')

        user = User.query.get_or_404(id)

        user = user.update(data)

        if user.profile:
            user.profile.update(profile_data)

            return user

        profile = Profile(**profile_data, user=user)
        profile.save()

        return user

    @staticmethod
    def update_identity(data, user):
        user.email = data['email']
        user.username = data['username']

        return user.save()

    @staticmethod
    def update_password(password, user):
        user.password = User.encrypt_password(password)

        return user.save()

    @staticmethod
    def update_profile(data, user):
        if user.profile:
            return user.profile.update(data)

        profile = Profile(**data, user=user)
        profile.save()

        return profile
