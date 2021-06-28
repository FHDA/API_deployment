from app import okta_helper
from flask import Flask, make_response, request
from functools import wraps


def access_token_required(func):
    """Decorator to check whether the request has valid access token.

    Wraps a function and check whether the incoming request has a vlid
    access token. If the access token is invalid, return a 403
    unauthorized error as response. Otherwise, pass to the original
    function with user id.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        (
            is_authorized,
            error_message_or_uid,
        ) = okta_helper.is_access_request_authorized(request)
        if is_authorized:
            return func(error_message_or_uid)
        else:
            return make_response(error_message_or_uid, 403)

    return decorated_view


def id_token_required(func):
    """Decorator to check whether the request has valid ID token.

    Wraps a function and check whether the incoming request has a vlid
    ID token. If the ID token is invalid, return a 403 unauthorized
    error as response. Otherwise, pass to the original function with
    user id.
    """

    @wraps(func)
    def decorated_view():
        (is_authorized, error_message_or_uid) = okta_helper.is_id_request_authorized(
            request
        )
        if is_authorized:
            return func(error_message_or_uid)
        else:
            return make_response(error_message_or_uid, 403)

    return decorated_view
