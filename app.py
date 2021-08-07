"""API component.

This module gets request from frontend and make corresponding responses
"""

from dotenv import load_dotenv, find_dotenv
from flask import Flask, abort, request, jsonify, render_template
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
import flask_restful
import os

app = Flask(__name__)
CORS(app)

# Load envvironmental variables in .env
load_dotenv(find_dotenv())

# Configure SQL Alchemy
import pymysql

pymysql.install_as_MySQLdb()

app.config["MYSQL_DATABASE_CHARSET"] = "utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    os.environ.get("sql_user"),
    os.environ.get("sql_password"),
    os.environ.get("sql_host"),
    os.environ.get("sql_port"),
    os.environ.get("sql_db_name"),
)

sql_db = SQLAlchemy(app)

# Setup Login Manager
from src.auth.okta_helper import OktaHelper

okta_helper = OktaHelper()
from src.auth.login_manager import (
    user_login_required,
    admin_login_required,
    superadmin_login_required,
)

# Intialize API Resource
from src.contact import ContactForm
from src.course import Course, CourseList
from src.department import Department, DepartmentList
from src.seat import Seat, SeatList
from src.story.article import Article
from src.story.miscellaneous import Hashtag
from src.story.comment import Comment
from src.auth.user import User
from src.story.article_like import Article_Like
from src.story.comment_like import Comment_Like

api = Api(app)
# Contact APIs
api.add_resource(ContactForm, "/contact")
# Course APIs
api.add_resource(Course, "/course")
api.add_resource(CourseList, "/course_list")
api.add_resource(Department, "/department")
api.add_resource(DepartmentList, "/department_list")
api.add_resource(SeatList, "/seat_list")
api.add_resource(Seat, "/seat")
# Story APIs
api.add_resource(Article, "/story")
api.add_resource(Hashtag, "/story/hashtag")
api.add_resource(Comment, "/story/comment")
api.add_resource(Article_Like, "/story/article_like")
api.add_resource(Comment_Like, "/story/comment_like")
# User APIs
api.add_resource(User, "/user")

# Some examples of using okta authorization login manager.
# Example 1: no login is needed.
@app.route("/")
def index():
    return render_template("index.html")


# Example 2: require user login.
@app.route("/example_user_check/<test_param>")
@user_login_required
def example_user_check(okta_id, uid, test_param):
    return render_template("index.html")


# Example 3: require admin login
@app.route("/example_admin_check/<test_param>")
@admin_login_required
def example_admin_check(okta_id, uid, test_param):
    return render_template("index.html")


# Example 4: require superadmin login
@app.route("/example_superadmin_check/<test_param>")
@superadmin_login_required
def example_superadmin_check(okta_id, uid, test_param):
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, ssl_context="adhoc")
