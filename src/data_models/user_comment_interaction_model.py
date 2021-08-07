from app import sql_db


class UserCommentInterationModel(sql_db.Model):
    __tablename__ = "user_comment_interaction"

    user_comment_interaction_id = sql_db.Column(
        sql_db.Integer,
        unique=True,
        nullable=False,
        autoincrement=True,
        primary_key=True,
    )
    user_id = sql_db.Column(sql_db.Integer, nullable=False)
    article_id = sql_db.Column(sql_db.Integer, nullable=False)
    mark_spam = sql_db.Column(sql_db.Boolean, default=False, nullable=False)
    like = sql_db.Column(sql_db.Boolean, default=False, nullable=False)