from flask_classful import FlaskView

from lib.classful_representations import output_json


class BaseView(FlaskView):
    representations = {'application/json': output_json}
