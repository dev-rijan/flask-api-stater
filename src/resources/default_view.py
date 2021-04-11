from flask import current_app
from flask_classful import route

from src.resources.base import BaseView


class DefaultView(BaseView):
    route_base = '/'

    def index(self):
        return {
            'title': 'Endo monitoring api',
            'version': current_app.config['FLASK_APP_VERSION']
        }

    @route('/healthy', methods=['GET'])
    def healthy(self):
        return 'healthy'
