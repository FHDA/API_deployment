import json
import sys

sys.path.append("..")

from app import sql_db
from flask import request
from flask_restful import reqparse, abort, Api, Resource
from src.auth.login_manager import user_login_required
from src.util import generate_response

parser = reqparse.RequestParser()


class User(Resource):
    @user_login_required
    def get(okta_id, user_id, self):
        """Get a user's user id by having id token in auth header.

        Args from request:
            None
        Return:
            User ID
        """
        return user_id
