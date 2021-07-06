from app import sql_db
import datetime


class UserArticleInteractionModel(sql_db.Model):
    __tablename__ = "user_article_interaction"
    user_article_interaction_id = sql_db.Column(
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
