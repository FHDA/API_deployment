import json
import sys

sys.path.append("..")

from app import sql_db
from datetime import datetime
from flask import request
from flask_restful import reqparse, abort, Api, Resource
from src.auth.login_manager import user_login_required
from src.util import generate_response
from src.data_models.user_comment_interaction_model import UserCommentInterationModel
from src.data_models.comment_model import CommentModel

parser = reqparse.RequestParser()
parser.add_argument("story_id")
parser.add_argument("user_id")
parser.add_argument("like_count")

class Comment_Like(Resource):
    @user_login_required
    def put(self, okta_id, user_id):
        """
        Update the count of likes for comment.
        Update the like count depends on if the user liked the comment before or not
        
        Args from request:
            story_id: 
            user_id:
            comment_id:
        Return:
            A response specifying whether the comment's like count update is successful or not.
        """
        args = parser.parse_args()

        if args["story_id"] is None or args["user_id"] is None or args["comment_id"] is None:
            return generate_response("Error: Invalid Parameters.", 400)
        if args["user_id"] != str(user_id):
            return generate_response("Error: Not Authorized.", 403)
        # update its like_count
        comment = CommentModel.query.filter_by(
            article_id = args["story_id"], user_id = user_id, comment_id = args["comment_id"]
        ).first()
        # update its like (boolean)
        user_comt_inter = UserCommentInterationModel.query.filter_by(
            user_id = user_id, article_id = args["article_id"]
        ).first()

        if user_comt_inter.mark_spam != True:
            if user_comt_inter.like:
                user_comt_inter.like = False
                comment.like_count = comment.like_count - 1
            else:
                user_comt_inter.like = True
                comment.like_count = comment.like_count + 1
        
        sql_db.session.commit()
        return generate_response("Success: Like Count Updated", 200)

        


        