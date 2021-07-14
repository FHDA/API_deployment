from app import okta_helper, sql_db
from datetime import datetime
from flask import Flask, make_response, request
from functools import wraps
from src.data_models.enum_tables.role import from_code_to_role_name
from src.data_models.user_model import UserModel


def get_user_id_and_role_from_okta_id(okta_id, create_user=True):
    """Get user ID and its role from okta ID.

    Search SQL database `user` table, if the okta_id exists, return the
    corresponding user id. Otherwise, create a new user in `user` table
    and return its user id and role.

    args:
        okta_id: str, okta unique id.
    return:
        user_id: int, the user_id corresponding to the okta_id in `user` table.
        role: str, the role type following role enum table.
    """
    user = UserModel.query.filter_by(okta_id=okta_id).first()
    if user is None:
        if create_user:
            user = UserModel(okta_id=okta_id, creation_time=datetime.now(), role=0)
            sql_db.session.add(user)
            sql_db.session.commit()
            return user.user_id, from_code_to_role_name(user.role)
        else:
            return None, None
    else:
        return user.user_id, from_code_to_role_name(user.role)


def user_login_required(func):
    """Decorator to check whether the request is from login user.

    Wraps a function and check whether the incoming request has a vlid
    ID token. If the ID token is invalid, return a 403 unauthorized
    error as response. Otherwise, pass to the original function with
    okta id and user id.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        (
            is_authorized,
            error_message_or_okta_id,
        ) = okta_helper.is_id_request_authorized(request)
        if is_authorized:
            return func(
                error_message_or_okta_id,
                get_user_id_and_role_from_okta_id(error_message_or_okta_id),
                *args,
                **kwargs
            )
        else:
            return make_response(error_message_or_okta_id, 403)

    return decorated_view


def admin_login_required(func):
    """Decorator to check whether the request is from login admin.

    Wraps a function and check whether the incoming request has a vlid
    ID token. If the ID token is invalid, return a 403 unauthorized
    error as response. Otherwise, pass to the original function with
    okta id and user id.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        (
            is_authorized,
            error_message_or_okta_id,
        ) = okta_helper.is_id_request_authorized(request)
        if is_authorized:
            user_id, role = get_user_id_and_role_from_okta_id(
                error_message_or_okta_id, create_user=False
            )
            if role != "Admin" and role != "SuperAdmin":
                return make_response("Role `admin` is required. ", 403)
            return func(error_message_or_okta_id, user_id, *args, **kwargs)
        else:
            return make_response(error_message_or_okta_id, 403)

    return decorated_view


def superadmin_login_required(func):
    """Decorator to check whether the request is from login super admin.

    Wraps a function and check whether the incoming request has a vlid
    ID token. If the ID token is invalid, return a 403 unauthorized
    error as response. Otherwise, pass to the original function with
    okta id and user id.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        (
            is_authorized,
            error_message_or_okta_id,
        ) = okta_helper.is_id_request_authorized(request)
        if is_authorized:
            user_id, role = get_user_id_and_role_from_okta_id(
                error_message_or_okta_id, create_user=False
            )
            if role != "SuperAdmin":
                return make_response("Role `super admin` is required. ", 403)
            return func(error_message_or_okta_id, user_id, *args, **kwargs)
        else:
            return make_response(error_message_or_okta_id, 403)

    return decorated_view
