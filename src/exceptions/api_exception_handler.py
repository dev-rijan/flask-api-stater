from werkzeug.exceptions import HTTPException
from flask import make_response, jsonify


class ApiExceptionHandler:
    def __init__(self, app):
        self.app = app
        self.register()

    def register(self):
        self.app.register_error_handler(
            HTTPException, self._handle_http_exception)

    def _handle_http_exception(self, exception: HTTPException):
        return make_response(
            jsonify(error=exception.description, code=exception.code), exception.code
        )
