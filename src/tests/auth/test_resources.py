import random

from flask import url_for

from config import settings
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
            'email': 'client@flask_api.com',
            'password': 'client@password'
        },
        {
            'email': 'client2@flask_api.com',
            'password': 'client2@password'
        }
    ]

    return random.choice(users)


class TestAuthResources(ResourceTestMixin):
    def test_login(self):
        """ Login successfully. """
        user = _get_random_user()
        response = self.login(identity=user['email'], password=user['password'])
        response_json = response.get_json()

        assert response.status_code == 200
        assert 'access_token' in response_json
        assert 'refresh_token' in response_json

    def test_login_disable(self):
        """ Login failure due to account being disabled. """
        response = self.login(identity='disabled@flask_api.com', password='disabled@password')

        assert response.status_code == 403

    def test_login_fail(self):
        """ Login failure due to invalid login credentials. """
        response = self.login(identity='incorrect@flask_api.com', password='incorrect@password')

        assert response.status_code == 401

    def test_logout(self):
        """ Logout successfully. """
        login_response = self.login()
        access_token_header = {'Authorization': 'Bearer {}'.format(login_response.get_json()['access_token'])}
        refresh_token_header = {'Authorization': 'Bearer {}'.format(login_response.get_json()['refresh_token'])}

        response = self.client.delete(url_for('AuthView:access_token_revoke'), headers=access_token_header)
        assert response.status_code == 200

        response = self.client.delete(url_for('AuthView:refresh_token_revoke'), headers=refresh_token_header)
        assert response.status_code == 200

        response = self.client.get(url_for('UsersView:index'))
        assert response.status_code == 401

    # def test_reset_password_request_fail(self):
    #     """ Request reset token failure due to using a non-existent account. """
    #     user = {'identity': 'invalid_user@flask_api.com'}
    #     response = self.client.post(url_for('AuthView:reset_password_request'), json=user)

    #     response.status_code = 422

    # def test_reset_password_request(self):
    #     """ Reset password request send successfully. """
    #     user = {'email': 'client@flask_api.com'}
    #     response = self.client.post(url_for('AuthView:reset_password_request'), json=user)
    #     assert response.status_code == 200

    # def test_password_reset(self, password_reset_token):
    #     """ Reset successful. """
    #     reset = {'password': 'newpassword'}
    #     response = self.client.post(url_for('AuthView:reset_password', token=password_reset_token), json=reset)

    #     assert response.status_code == 200
    #     assert response.get_json()['success'] is True

    #     client = User.find_by_identity('client@flask_api.com')
    #     assert client.password != reset['password']

    # def test_password_reset_invalid_token(self):
    #     """ Reset failure due to tampered reset token. """
    #     reset = {'password': 'newpassword'}
    #     response = self.client.post(url_for('AuthView:reset_password', token='tempered-token'), json=reset)

    #     assert response.status_code == 403
