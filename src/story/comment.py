import json
import sys

sys.path.append("..")

from app import sql_db
from datetime import datetime
from flask import request
from flask_restful import reqparse, abort, Api, Resource
from src.auth.login_manager import access_token_required, id_token_required
from src.util import generate_response
from src.data_models.comment_model import CommentModel

parser = reqparse.RequestParser()
parser.add_argument("story_id")
parser.add_argument("user_id")
parser.add_argument("comment_id")


def get_comments(article_id, user_id, comment_id):
    """Get comments filtered by article_id, user_id, comment_id if available.

    Send request to SQL database to get comments based on article_id,
    user_id, comment_id. If an ID is not available, then skip this when
    filtering.

    Args:
        article_id: int, unique article id
        user_id: int, unique user id
        comment_id: int, unique comment id
    Return:
        A list of comment dictionary.
    """
    args = {}
    if article_id:
        args["article_id"] = article_id
    if user_id:
        args["user_id"] = user_id
    if comment_id:
        args["comment_id"] = comment_id
    comments = CommentModel.query.filter_by(**args).all()
    return [comment.to_dict() for comment in comments]


class Comment(Resource):
    @access_token_required
    def get(self):
        """Get comments from SQL database.

        Args from request:
            story_id: int, unique article id
            user_id: int, unique user id
            comment_id: int, unique comment id
        Return:
            A list of comment dictionary.
        """
        request.get_json()
        args = parser.parse_args()
        if args["story_id"] is None:
            return generate_response("Error: Story ID not found. ", 400)
        return generate_response(
            get_comments(args["story_id"], args["user_id"], args["comment_id"]), 200
        )

    @id_token_required
    def post(okta_id, user_id, self):
        """Create a new comment post.

        Args from request:
            story_id: int, unique article id
            user_id: int, unique user id
            comment_content: str, the content of comment(in request body)
        Return:
            A response specifying whether the comment creation is successed.
        """
        args = parser.parse_args()
        if args["story_id"] is None or args["user_id"] is None:
            return generate_response("Error: Invalid parameters.", 400)
        if args["user_id"] != str(user_id):
            return generate_response("Error: Not Authorized.", 403)
        request_data = json.loads(request.get_data())
        if "comment_content" not in request_data:
            return generate_response("Error: Comment can not be empty.", 400)
        new_comment = CommentModel(
            comment_content=request_data["comment_content"],
            user_id=user_id,
            article_id=args["story_id"],
            post_time=datetime.now(),
            like_count=0,
            is_spam=False,
        )
        sql_db.session.add(new_comment)
        sql_db.session.commit()
        return generate_response("Success: Comment Created. ", 200)

    @id_token_required
    def put(okta_id, user_id, self):
        """Update the content of a current comment post.

        Args from request:
            story_id: int, unique article id
            user_id: int, unique user id
            comment_id: int, unique comment id
            comment_content: str, the content of comment(in request body)
        Return:
            A response specifying whether the comment update is successed.
        """
        args = parser.parse_args()
        if (
            args["story_id"] is None
            or args["user_id"] is None
            or args["comment_id"] is None
        ):
            return generate_response("Error: Invalid Parameters.", 400)
        if args["user_id"] != str(user_id):
            return generate_response("Error: Not Authorized.", 403)
        request_data = json.loads(request.get_data())
        if "comment_content" not in request_data:
            return generate_response("Error: Comment can not be empty.", 400)
        comment = CommentModel.query.filter_by(
            article_id=args["story_id"], user_id=user_id, comment_id=args["comment_id"]
        ).first()
        comment.comment_content = request_data["comment_content"]
        sql_db.session.commit()
        return generate_response("Success: Comment Content Updated. ", 200)

    @id_token_required
    def delete(okta_id, user_id, self):
        """Delete a comment.

        Args from request:
            story_id: int, unique article id
            user_id: int, unique user id
            comment_id: int, unique comment id
        Return:
            A response specifying whether the comment deletion is successed.
        """
        args = parser.parse_args()
        if (
            args["story_id"] is None
            or args["user_id"] is None
            or args["comment_id"] is None
        ):
            return generate_response("Error: Invalid Parameters.", 400)
        if args["user_id"] != str(user_id):
            return generate_response("Error: Not Authorized.", 403)
        comment = CommentModel.query.filter_by(
            article_id=args["story_id"], user_id=user_id, comment_id=args["comment_id"]
        ).first()
        sql_db.session.delete(comment)
        sql_db.session.commit()
        return generate_response("Success: Comment Deleted. ", 200)
