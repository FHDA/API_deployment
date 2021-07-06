from app import sql_db
import datetime


class CommentModel(sql_db.Model):
    __tablename__ = "comment"
    comment_id = sql_db.Column(
        sql_db.Integer,
        unique=True,
        nullable=False,
        autoincrement=True,
        primary_key=True,
    )
    comment_content = sql_db.Column(sql_db.String(1000))
    user_id = sql_db.Column(sql_db.Integer, nullable=False)
    quote_id = sql_db.Column(sql_db.Integer, nullable=False)
    article_id = sql_db.Column(sql_db.Integer, nullable=False)
    post_time = sql_db.Column(sql_db.DateTime, nullable=False)
    like_count = sql_db.Column(sql_db.Integer, nullable=False)
    is_spam = sql_db.Column(sql_db.Boolean, default=False, nullable=False)
