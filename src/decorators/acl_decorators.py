from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, current_user

from src.models.user import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        if current_user.role != User.ROLE_ADMIN:
            return jsonify(message='This user don\'t have permission to access this resource'), 403

        if not current_user.is_active:
            return jsonify(message='This user is disable, please contact admin'), 401

        return fn(*args, **kwargs)

    return wrapper


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()

        if not current_user.is_active:
            return jsonify(message='This user is disable, please contact admin'), 401

        return fn(*args, **kwargs)

    return wrapper
