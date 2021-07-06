from app import sql_db
import datetime


class ArticleModel(sql_db.Model):
    __tablename__ = "article"

    article_id = sql_db.Column(
        sql_db.Integer,
        unique=True,
        nullable=False,
        autoincrement=True,
        primary_key=True,
    )
    article_title = sql_db.Column(sql_db.String(500))
    article_content = sql_db.Column(sql_db.String(5000))
    user_id = sql_db.Column(sql_db.Integer, nullable=False)
    like_count = sql_db.Column(sql_db.Integer, nullable=False)
    view_count = sql_db.Column(sql_db.Integer, nullable=False)
    click_count = sql_db.Column(sql_db.Integer, nullable=False)
    post_time = sql_db.Column(sql_db.DateTime, nullable=False)
    last_updated_time = sql_db.Column(sql_db.DateTime, nullable=False)
    school_from = sql_db.Column(sql_db.Integer)
    school_to = sql_db.Column(sql_db.Integer)
    major = sql_db.Column(sql_db.Integer)
    graduate_year = sql_db.Column(sql_db.Integer)
    degree_type = sql_db.Column(sql_db.Integer)
    is_spam = sql_db.Column(sql_db.Boolean, default=False, nullable=False)
    is_approved = sql_db.Column(sql_db.Boolean, default=False, nullable=False)
