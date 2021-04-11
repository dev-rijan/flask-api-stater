import random

from flask import url_for

from config import settings
from src.models.user import User
from src.services.user import UserService
from src.tests.utils import ResourceTestMixin


def _get_random_user():
    """
    return random user
    """
    users = [
        {
            'email': settings.SEED_ADMIN_EMAIL,
            'password': settings.SEED_ADMIN_PASSWORD
        },
        {
            'email': 'client@endo.com',
            'password': 'client@password'
        },
        {
            'email': 'client2@endo.com',
            'password': 'client2@password'
        },
        {
            'email': 'iot@endo.com',
            'password': 'iot@password'
        }
    ]

    return random.choice(users)


class TestUserResources(ResourceTestMixin):
    def test_unauthorized_user_access(self):
        """
        All users routes should respond with a error 401 for unauthorized user
        """
        response = self.client.get(url_for('UsersView:index'))
        assert response.status_code == 401

        response = self.client.get(url_for('UsersView:get', id=1))
        assert response.status_code == 401

        response = self.client.post(url_for('UsersView:post'))
        assert response.status_code == 401

        response = self.client.put(url_for('UsersView:put', id=1))
        assert response.status_code == 401

        response = self.client.post(url_for('UsersView:disable', id=1))
        assert response.status_code == 401

        response = self.client.post(url_for('UsersView:enable', id=1))
        assert response.status_code == 401

        response = self.client.post(url_for('UsersView:update_identity'))
        assert response.status_code == 401

        response = self.client.post(url_for('UsersView:update_password'))
        assert response.status_code == 401

        response = self.client.post(url_for('UsersView:update_profile'))
        assert response.status_code == 401

    def test_client_user_access_users_list(self):
        """
        Client user cant not access users list, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='client@endo.com', password='client@password')

        response = self.client.get(url_for('UsersView:index'), headers=headers)
        assert response.status_code == 403

    def test_iot_user_access_users_list(self):
        """
        IoT user cant not access users list, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='iot@endo.com', password='iot@password')

        response = self.client.get(url_for('UsersView:index'), headers=headers)
        assert response.status_code == 403

    def test_client_user_access_user(self):
        """
        Client user cant not access user, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='client@endo.com', password='client@password')

        response = self.client.get(url_for('UsersView:get', id=2), headers=headers)
        assert response.status_code == 403

    def test_iot_user_access_user(self):
        """
        IOT user cant not access user, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='iot@endo.com', password='iot@password')

        response = self.client.get(url_for('UsersView:get', id=2), headers=headers)
        assert response.status_code == 403

    def test_client_can_not_create_user(self):
        """
        Client user cant not create user, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='client@endo.com', password='client@password')

        response = self.client.post(url_for('UsersView:post'), headers=headers)
        assert response.status_code == 403

    def test_iot_can_not_create_user(self):
        """
        IOT user cant not create user, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='iot@endo.com', password='iot@password')

        response = self.client.post(url_for('UsersView:post'), headers=headers)
        assert response.status_code == 403

    def test_client_can_not_update_user(self):
        """
        Client user cant not update specific user, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='client@endo.com', password='client@password')

        response = self.client.put(url_for('UsersView:put', id=1), headers=headers)
        assert response.status_code == 403

    def test_iot_can_not_update_user(self):
        """
        IOT user cant not update specific user, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='iot@endo.com', password='iot@password')

        response = self.client.put(url_for('UsersView:put', id=1), headers=headers)
        assert response.status_code == 403

    def test_client_can_not_disable_user(self):
        """
        Client user cant not disable specific user, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='client@endo.com', password='client@password')

        response = self.client.post(url_for('UsersView:disable', id=1), headers=headers)
        assert response.status_code == 403

    def test_iot_can_not_disable_user(self):
        """
        IOT user cant not disable specific user, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='iot@endo.com', password='iot@password')

        response = self.client.post(url_for('UsersView:disable', id=1), headers=headers)
        assert response.status_code == 403

    def test_client_can_not_enable_user(self):
        """
        Client user cant not disable specific user, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='client@endo.com', password='client@password')

        response = self.client.post(url_for('UsersView:enable', id=1), headers=headers)
        assert response.status_code == 403

    def test_iot_can_not_enable_user(self):
        """
        IOT user cant not disable specific user, should respond with 403(Forbidden) status
        """
        headers = self.get_authorization_header(identity='iot@endo.com', password='iot@password')

        response = self.client.post(url_for('UsersView:enable', id=1), headers=headers)
        assert response.status_code == 403

    def test_update_identity(self):
        """
        User should be able to update own identity
        """
        user = _get_random_user()

        headers = self.get_authorization_header(identity=user['email'], password=user['password'])
        data = {
            'email': 'updatedEmail@endo.com',
            'username': 'updatedUsername'
        }

        response = self.client.post(url_for('UsersView:update_identity'), json=data, headers=headers)
        actual_result = response.get_json()['user']
        assert response.status_code == 200
        assert data['email'] == actual_result['email']
        assert data['username'] == actual_result['username']

    def test_update_password(self):
        """
        User should be able to update own password
        """
        user = _get_random_user()

        headers = self.get_authorization_header(identity=user['email'], password=user['password'])
        data = {
            'current_password': user['password'],
            'new_password': 'updatedPassword'
        }

        response = self.client.post(url_for('UsersView:update_password'), json=data, headers=headers)
        assert response.status_code == 200
        assert response.get_json()['success'] is True

    def test_update_profile(self):
        """
        User should be able to update own profile
        """

        user = _get_random_user()

        headers = self.get_authorization_header(identity=user['email'], password=user['password'])
        data = {
            'name': 'updated_name',
            'name_kana': 'updated_name_kana'
        }

        response = self.client.post(url_for('UsersView:update_profile'), json=data, headers=headers)
        updated_profile = response.get_json()['profile']

        assert response.status_code == 200
        assert data['name'] == updated_profile['name']
        assert data['name_kana'] == updated_profile['name_kana']

    def test_users_list(self):
        """
        Only admin can access users list
        """
        headers = self.get_authorization_header()

        response = self.client.get(url_for('UsersView:index'), headers=headers)
        assert response.status_code == 200

        # users count should same to users created on fixture
        assert len(response.get_json()['users']) == 5

    def test_get_user(self):
        """
        Only admin can access user
        """
        headers = self.get_authorization_header()

        user_id = random.choice([1, 2, 3, 4, 5])
        response = self.client.get(url_for('UsersView:get', id=user_id), headers=headers)

        assert response.status_code == 200

    def test_user_create(self):
        """
        Only admin can create user
        """
        headers = self.get_authorization_header()
        data = {
            'role': random.choice([*User.ROLES.values()]),
            'email': 'new_user@endo.com',
            'username': 'new_user',
            'password': 'new_user@password',
            'profile': {
                'name': 'new user name',
                'name_kana': 'new user kana'
            }
        }

        response = self.client.post(url_for('UsersView:post'), json=data, headers=headers)
        actual_result = response.get_json()['user']
        # remove id from actual result to compare with expected result
        actual_result.pop('id')
        actual_result.get('profile').pop('id')

        # remove password from data to compare with actual result
        data.pop('password')
        expected_result = {**data, 'is_active': True}

        assert response.status_code == 200
        assert expected_result == actual_result

    def test_user_update(self):
        """
        Only admin can update user
        """
        headers = self.get_authorization_header()
        user = random.choice(UserService.get_all())

        data = {
            'id': user.id,
            'role': random.choice([*User.ROLES.values()]),
            'email': 'updated_user@endo.com',
            'username': 'updated_user',
            'profile': {
                'id': user.id,
                'name': 'updated user name',
                'name_kana': 'updated user kana'
            }
        }

        response = self.client.put(url_for('UsersView:put', id=user.id), json=data, headers=headers)
        actual_result = response.get_json()['user']

        expected_result = {**data, 'is_active': user.is_active}

        assert response.status_code == 200
        assert expected_result == actual_result

    def test_user_disable(self):
        """
        Only admin can disable user
        """
        headers = self.get_authorization_header()
        user = random.choice(UserService.get_all())

        response = self.client.post(url_for('UsersView:disable', id=user.id), headers=headers)
        actual_result = response.get_json()['user']

        assert response.status_code == 200
        assert actual_result['is_active'] is False

    def test_user_enable(self):
        """
        Only admin can enable user
        """
        headers = self.get_authorization_header()
        user = random.choice(UserService.get_all())

        response = self.client.post(url_for('UsersView:enable', id=user.id), headers=headers)
        actual_result = response.get_json()['user']

        assert response.status_code == 200
        assert actual_result['is_active'] is True
