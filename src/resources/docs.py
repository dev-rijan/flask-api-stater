from src.resources.base import BaseView
from flask_classful import route
from flask import current_app
from flask import jsonify
from flask import render_template
from src.extensions import apispec
from flask_classful import FlaskView


class DocsView(FlaskView):
    def index(self):
        return render_template('docs/swaggerui.html')

    @route('/json')
    def json(self):
        return jsonify(apispec.to_dict()), 200
