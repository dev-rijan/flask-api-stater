import pytest
from flask import url_for
from config import settings


class ResourceTestMixin(object):
    """
    Automatically load in a session and client, this is common for a lot of
    tests that work with resources.
   """

    @pytest.fixture(autouse=True)
    def set_common_fixtures(self, session, client, users):
        self.session = session
        self.client = client
        self.users = users

    def get_authorization_header(self, identity=settings.SEED_ADMIN_EMAIL, password=settings.SEED_ADMIN_PASSWORD):
        """
        Get access token by log in specific user and creates header

        :param identity: Username or Email
        :type identity: str
        :param password: Password
        :type password: str
        :return: Authorization header
        """

        response = self.login(identity, password)

        return {'Authorization': 'Bearer {}'.format(response.get_json()['access_token'])}

    def login(self, identity=settings.SEED_ADMIN_EMAIL, password=settings.SEED_ADMIN_PASSWORD):
        """
        Log a specific user in.

        :param identity: Username or Email
        :type identity: str
        :param password: Password
        :type password: str
        :return: Flask json response
        """

        user = dict(email=identity, password=password)

        response = self.client.post(url_for('AuthView:login'), json=user)

        return response

    def logout(self):
        """
        Logout a specific user.

        :return: Flask Json
        """
        pass
