import json
import sys

sys.path.append("..")

from app import sql_db
from datetime import datetime
from flask import request
from flask_restful import reqparse, abort, Api, Resource
from src.auth.login_manager import user_login_required
from src.util import generate_response
from src.data_models.user_article_interaction_model import UserArticleInteractionModel
from src.data_models.article_model import ArticleModel

parser = reqparse.RequestParser()
parser.add_argument("story_id")
parser.add_argument("user_id")
parser.add_argument("like_count")


class Article_Like(Resource):
    @user_login_required
    def put(self, okta_id, user_id):
        """
        Update the count of likes.
        Update the like count depends on if user liked the article before or not
        If the like (boolean) is True, then decrease the like count and return the like to False.

        Args from request:
            article_id: int, unique article id
            user_id: int, unique user id
            article_content: str, the content of article(in request body)
        Return:
            A response specifying whether the like count update is successful or not.
        """
        args = parser.parse_args()
        
        if args["article_id"] is None or args["user_id"] is None:
            return generate_response("Error: Invalid Parameters.", 400)

        if args["user_id"] != str(user_id):
            return generate_response("Error: Not Authorized.", 403)

        try:
            request_data = json.loads(request.get_data())
        except:
            return generate_response("Error: Invalid Request Body.", 400)

        # update its like_count
        article = ArticleModel.query.filter_by(
            user_id = user_id, article_id = args["article_id"]
        ).first()
        # update its like (boolean)
        user_art_inter = UserArticleInteractionModel.query.filter_by(
            user_id = user_id, article_id = args["article_id"]
        ).first()

        if user_art_inter.like:
            user_art_inter.like = False
            article.like_count = article.like_count - 1
        else: 
            user_art_inter.like = True
            article.like_count = article.like_count + 1
        
        sql_db.session.commit()
        return generate_response("Success: Like Count Updated", 200)
