from app import sql_db
import datetime


class UserModel(sql_db.Model):
    __tablename__ = "user"

    user_id = sql_db.Column(
        sql_db.Integer,
        unique=True,
        nullable=False,
        autoincrement=True,
        primary_key=True,
    )
    okta_id = sql_db.Column(sql_db.String(200), unique=True, nullable=False)
    role = sql_db.Column(sql_db.Integer, nullable=False)
    creation_time = sql_db.Column(sql_db.DateTime, nullable=False)
