import json
import sys

sys.path.append("..")

from app import sql_db
from datetime import datetime
from flask import request
from flask_restful import reqparse, abort, Api, Resource
from src.auth.login_manager import access_token_required, id_token_required
from src.util import generate_response
from src.data_models.article_model import ArticleModel

parser = reqparse.RequestParser()
parser.add_argument("story_id")
parser.add_argument("user_id")


def get_articles(user_id, article_id=None):
    """Get articles filtered by article_id, user_id if available.

    Send request to SQL database to get articles based on article_id,
    user_id. If no article_id is parsed, we return all articles

    Args:
        article_id: int, unique article id
        user_id: int, unique user id
    Return:
        A list of article dictionary.
    """
    args = {}
    if article_id:
        args["article_id"] = article_id
    if user_id:
        args["user_id"] = user_id
    articles = ArticleModel.query.filter_by(**args).all()
    return [article.to_dict() for article in articles]


class Article(Resource):
    @access_token_required
    def get(self):
        """Get story articles from SQL database.

        Args from request:
            story_id: int, unique article id
            user_id: int, unique user id
        Return:
            A list of article dictionary.
        """
        request.get_json()
        args = parser.parse_args()
        return generate_response(get_articles(args["user_id"], args["story_id"]), 200)

    @id_token_required
    def post(okta_id, user_id, self):
        """Create a new Article post.

        Args from request:
            story_id: int, unique article id
            user_id: int, unique user id
            article_title: str, the title of the article(in request body)
            article_content: str, the content of article(in request body)
            school_from: str, the school trasfer from(optional in request body)
            school_to: str, the school trasfer to(optional in request body)
            major: str, the major of the student(optional in request body)
            degree_type: int, the degree type of the student(optional in request body)
            graduate_year: int, the graduate year of the student(optional in request body)
        Return:
            A response specifying whether the article creation is successed.
        """
        args = parser.parse_args()
        if args["user_id"] is None:
            return generate_response("Error: Invalid Parameters.", 400)
        if args["user_id"] != str(user_id):
            return generate_response("Error: Not Authorized.", 403)
        try:
            request_data = json.loads(request.get_data())
        except:
            return generate_response("Error: Invalid Request Body.", 400)
        if "article_content" not in request_data:
            return generate_response("Error: Article content can not be empty.", 400)
        if "article_title" not in request_data:
            return generate_response("Error: Article title can not be empty.", 400)
        try:
            new_article = ArticleModel(
                article_content=request_data["article_content"],
                article_title=request_data["article_title"],
                user_id=user_id,
                post_time=datetime.now(),
                last_updated_time=datetime.now(),
                like_count=0,
                view_count=0,
                click_count=0,
                school_from=int(request_data.get("school_from", 0)),
                school_to=int(request_data.get("school_to", 0)),
                major=int(request_data.get("major", 0)),
                graduate_year=int(request_data.get("graduate_year", 0)),
                degree_type=int(request_data.get("degree_type", 0)),
                is_spam=False,
                is_approved=False,
            )
        except:
            return generate_response("Error: Invalid Parameters.", 400)
        sql_db.session.add(new_article)
        sql_db.session.commit()
        return generate_response("Success: Article Created. ", 200)

    @id_token_required
    def put(okta_id, user_id, self):
        """Update the content of a current article post.

        Args from request:
            story_id: int, unique article id
            user_id: int, unique user id
            article_content: str, the content of article(in request body)
        Return:
            A response specifying whether the article update is successed.
        """
        args = parser.parse_args()
        if args["story_id"] is None or args["user_id"] is None:
            return generate_response("Error: Invalid Parameters.", 400)
        if args["user_id"] != str(user_id):
            return generate_response("Error: Not Authorized.", 403)
        try:
            request_data = json.loads(request.get_data())
        except:
            return generate_response("Error: Invalid Request Body.", 400)
        if "article_content" not in request_data:
            return generate_response("Error: Article can not be empty.", 400)
        article = ArticleModel.query.filter_by(
            article_id=args["story_id"], user_id=user_id
        ).first()
        article.article_content = request_data["article_content"]
        sql_db.session.commit()
        return generate_response("Success: Article Content Updated. ", 200)

    @id_token_required
    def delete(okta_id, user_id, self):
        """Delete an article.

        Args from request:
            story_id: int, unique article id
            user_id: int, unique user id
        Return:
            A response specifying whether the article deletion is successed.
        """
        args = parser.parse_args()
        if args["story_id"] is None or args["user_id"] is None:
            return generate_response("Error: Invalid Parameters.", 400)
        if args["user_id"] != str(user_id):
            return generate_response("Error: Not Authorized.", 403)
        article = ArticleModel.query.filter_by(
            article_id=args["story_id"], user_id=user_id
        ).first()
        sql_db.session.delete(article)
        sql_db.session.commit()
        return generate_response("Success: Article Deleted. ", 200)
