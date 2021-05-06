from werkzeug import exceptions
from flask import make_response, jsonify


class ApiExceptionHandler:
    def __init__(self, app):
        self.app = app
        self.register()

    def register(self):
        self.app.register_error_handler(
            exceptions.TooManyRequests, self._handle_to_many_request)

    def _handle_to_many_request(self, exception):
        return make_response(
            jsonify(error="ratelimit exceeded %s" %
                    exception.description), exceptions.TooManyRequests.code
        )
