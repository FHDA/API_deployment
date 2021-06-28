from app import *
from configparser import ConfigParser
from okta_jwt_verifier import JWTVerifier
import asyncio
import os

loop = asyncio.get_event_loop()


class OktaHelper:

    """Okta token authorization helper.

    The okta token authorization helper will use okta jwt verifier
    library to verify whether an access token or id token is valid.

    Attributes:
        okta_configs: A dictionary of okta configs from `config/setup.cfg`.
                      The key is a string field name such as `auth_uri`,
                      and the value is corresponding config value.
    """

    def __init__(self):
        """Initialize okta config.

        Initialize okta config parsing project config file and fetch okta config.
        """

        configs = ConfigParser()
        configs.read(
            os.path.dirname(os.path.abspath(__file__)) + "/../../config/setup.cfg"
        )
        self.okta_configs = configs["okta"]

    def is_access_token_valid(self, token):
        """Check whether an access token is valid.

        Args:
            token: str, okta access token

        Returns:
            bool, whether the okta access token is valid.
            str, the user id if exists. Otherwise, return None.
        """

        jwt_verifier = JWTVerifier(
            self.okta_configs["issuer"], self.okta_configs["client_id"], "api://default"
        )
        try:
            loop.run_until_complete(jwt_verifier.verify_access_token(token))
            (headers, claims, signing_input, signature) = jwt_verifier.parse_token(
                token
            )
            return (True, claims["uid"])
        except Exception:
            return (False, None)

    def is_access_request_authorized(self, request):
        """Check whether a request has valid access token.

        Args:
            request: the flask request objrect

        Returns:
            bool, whether the okta access token is valid.
            str, the user id if exists. Otherwise, return None.
        """

        try:
            token = request.headers.get("Authorization").split("Bearer ")[1]
        except Exception:
            return (False, "Can not get authorization token from request.")
        (is_authorized, uid) = self.is_access_token_valid(token)
        if not is_authorized:
            return (False, "Access token is invalid")
        return (True, uid)

    def is_id_token_valid(self, token):
        """Check whether an ID token is valid.

        Args:
            token: str, okta ID token

        Returns:
            bool, whether the okta ID token is valid.
            str, the user id if exists. Otherwise, return None.
        """

        jwt_verifier = JWTVerifier(
            self.okta_configs["issuer"], self.okta_configs["client_id"], "api://default"
        )
        try:
            (headers, claims, signing_input, signature) = jwt_verifier.parse_token(
                token
            )
            loop.run_until_complete(
                jwt_verifier.verify_id_token(token, nonce=claims["nonce"])
            )
            return (True, claims["sub"])
        except Exception:
            return (False, None)

    def is_id_request_authorized(self, request):
        """Check whether a request has valid ID token.

        Args:
            request: the flask request objrect

        Returns:
            bool, whether the okta ID token is valid.
            str, the user id if exists. Otherwise, return None.
        """

        try:
            token = request.headers.get("Authorization").split("Bearer ")[1]
        except Exception:
            return (False, "Can not get authorization token from request.")
        (is_authorized, sub) = self.is_id_token_valid(token)
        if not is_authorized:
            return (False, "ID token is invalid")
        return (True, sub)
