from app import sql_db
from src.data_models.enum_tables.degree_type import from_code_to_degree_type_name
from src.data_models.enum_tables.school import from_code_to_school_name
from src.data_models.enum_tables.major import from_code_to_major_name
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

    def to_dict(self):
        """Convert current article to dictionary format.

        Returns:
            A dictionary that includes all columns and its values of
            a article in the `article` table.
        """
        return {
            "article_id": self.article_id,
            "article_title": self.article_title,
            "article_content": self.article_content,
            "user_id": self.user_id,
            "like_count": self.like_count,
            "view_count": self.view_count,
            "post_time": str(self.post_time),
            "last_updated_time": str(self.last_updated_time),
            "school_from": {
                "school_code": self.school_from,
                "name": from_code_to_school_name(self.school_from),
            },
            "school_to": {
                "school_code": self.school_to,
                "name": from_code_to_school_name(self.school_to),
            },
            "major": {
                "major_code": self.major,
                "name": from_code_to_major_name(self.major),
            },
            "graduate_year": self.graduate_year,
            "degree_type": {
                "degree_type_code": self.degree_type,
                "name": from_code_to_degree_type_name(self.degree_type),
            },
            "is_spam": self.is_spam,
            "is_approved": self.is_approved,
        }
