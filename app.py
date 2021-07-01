"""API component.

This module gets request from frontend and make corresponding responses
"""

from dotenv import load_dotenv, find_dotenv
from flask import Flask, abort, request, jsonify, render_template
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource
from src.auth.okta_helper import *
from src.contact import ContactForm
from src.course import Course, CourseList
from src.department import Department, DepartmentList
from src.seat import Seat, SeatList
import flask_restful

app = Flask(__name__)
CORS(app)

# Intialize API Resource
api = Api(app)
api.add_resource(ContactForm, "/contact")
api.add_resource(Course, "/course")
api.add_resource(CourseList, "/course_list")
api.add_resource(Department, "/department")
api.add_resource(DepartmentList, "/department_list")
api.add_resource(SeatList, "/seat_list")
api.add_resource(Seat, "/seat")

# Load envvironmental variables in .env
load_dotenv(find_dotenv())

# Setup Login Manager
okta_helper = OktaHelper()
from src.auth.login_manager import access_token_required, id_token_required


# Some examples of using okta authorization login manager.
# Example 1: no login is needed.
@app.route("/")
def index():
    return render_template("index.html")


# Example 2: require valid access token.
@app.route("/example_access_token_check")
@access_token_required
def example_access_token_check(uid):
    return render_template("index.html")


# Example 3: require valid ID token.
@app.route("/example_id_token_check")
@id_token_required
def example_id_token_check(uid):
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, ssl_context="adhoc")
