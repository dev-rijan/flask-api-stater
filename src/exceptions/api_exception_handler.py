from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException, UnprocessableEntity
from flask import jsonify


class ApiExceptionHandler:
    def __init__(self, app):
        self.app = app
        self.register()

    def register(self):
        self.app.register_error_handler(
            HTTPException, self._handle_http_exception)
        self.app.register_error_handler(
            UnprocessableEntity, self._handle_unprocessable_exception)

    def _handle_http_exception(self, exception: HTTPException):
        return jsonify(error=exception.description, code=exception.code), exception.code

    def _handle_unprocessable_exception(self, exception: ValidationError):
        messages = exception.data.get('messages', ['Invalid request.'])
        return jsonify(error=exception.description, code=exception.code, fields=messages.get('json', messages)), exception.code
