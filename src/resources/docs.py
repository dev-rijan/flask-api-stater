from src.resources.base import BaseView
from flask_classful import route
from flask import current_app
from flask import jsonify
from flask import render_template
from src.extensions import apispec
from src.resources.base import BaseView


class DocsView(BaseView):
    def index(self):
        return render_template('swaggerui.html')

    @route('/json')
    def json():
        return apispec.to_dict(), 200
