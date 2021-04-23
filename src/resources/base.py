from flask_classful import FlaskView

from src.utils.classful_representations import output_json


class BaseView(FlaskView):
    representations = {'application/json': output_json}
