# -*- coding: utf-8 -*-
"""API component.

This module gets request from frontend and make corresponding responses
"""
import json, os, sys, letslog
from flask import Flask, abort, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from configparser import ConfigParser
from pymongo import MongoClient
from pymongo import errors as mongoerrors
from bson.json_util import dumps, loads

app = Flask(__name__)
api = Api(app)
env_config = ConfigParser()
env_config.read(os.path.dirname(os.path.abspath(__file__))+'\\..\\config\\setting.config')
mongo_config = env_config['MongoDB']

def get_db():
    """Get MongoDB username and password from the config file and return the desired database.

    Raises:
        pymongo.errors: possibly connection errors or conficuration errors
    Returns:
        The database object

    """
    username, password = mongo_config['Mongo_User'], mongo_config['Mongo_Password']
    db_name = mongo_config['Mongo_DBName']
    client = MongoClient('mongodb+srv://' + username + ':' + password+ mongo_config['Mongo_Postfix'])
    return client.get_database(db_name)
db = get_db()

def abort_if_course_doesnt_exist(course_id, courses, year=None, quarter=None):
    """Send error message if course does not exist.

    Send corresponding error message if a requested course does not exist

    Args:
        course_id: the crn of the course requested
        courses: the dictionary of courses loaded from db
        year: the year of the requested quarter
        quarter: the requested quarter
    Returns:
        None

    """
    if course_id not in courses:
        if year and quarter:
            abort(404, message="Not Found(404): Course {0} doesn't exist in quarter {1} {2}".format(course_id, year, quarter))
        else:
            abort(404, message="Not Found(404): Course {} doesn't exist".format(course_id))

def abort_invalid_input(err_message):
    """Send an error message 400.
    """
    abort(400, message=err_message)

def abort_not_found(err_message):
    """Send an error message 404.
    """
    abort(404, message=err_message)

def get_quarter_collections(year, quarter, collection_type):
    """Get the collection from db according to defined quarter and the type of collection requested.

    Args:
        year: the year of the requested quarter
        quarter: the requested quarter
        collection_type: str, either "courses" or "departments"
    Returns:
        The collection received from db

    """
    collection_name = str(year) + " " + quarter + " De Anza " + collection_type
    coll = db.get_collection(collection_name)
    if coll.count() == 0:
        abort(404, message="Not Found(404): Database collection entry {} doesn't exist".format(collection_name))
    return coll



parser = reqparse.RequestParser()
parser.add_argument('year')
parser.add_argument('quarter')
parser.add_argument('department')
parser.add_argument('course_id')

class course(Resource):
    def get_by_quarter(self, year, quarter, course_id):
        """Get the course with defined course_id from defined quarter.

        Args:
            year: the year of the requested quarter
            quarter: the requested quarter
            course_id: the crn of the course requested
        Returns:
            The course with defined course_id from defined quarter

        """
        coll = get_quarter_collections(year, quarter, "courses")
        courses = coll.find({"UID": course_id})
        courses = json.loads(dumps(list(courses)))
        courses = {course['UID']:course for course in courses}
        abort_if_course_doesnt_exist(course_id, courses, year, quarter)
        return courses[course_id]

    def get(self):
        """The function that execute when receiving a course get request.

        Args(from request body):
            year: the year of the requested quarter
            quarter: the requested quarter
            course_id: the crn of the course requested
        Returns:
            The course with defined course_id from defined quarter

        """
        request.get_json()
        args = parser.parse_args()
        try:
            year = int(args['year'])
            quarter = str(args['quarter'])
            department = str(args['department'])
            course_id = str(args['course_id'])
        except:
            abort_invalid_input("Invalid Input(400): Please check you input parameters!")
        if year and quarter!="None" and course_id!="None":
            return self.get_by_quarter(year, quarter, course_id)
        else:
            abort_invalid_input("Invalid Input(400): Please provide all parameters to proceed!")

class courseList(Resource):
    def get_by_quarter(self, year, quarter):
        """Get the dictionary of courses from defined quarter.

        Args:
            year: the year of the requested quarter
            quarter: the requested quarter
        Returns:
            The dictionary of courses from defined quarter

        """
        coll = get_quarter_collections(year, quarter, "courses")
        courses = coll.find()
        courses = json.loads(dumps(list(courses)))
        courses = {course['UID']:course for course in courses}
        return courses

    def get_by_quarter_department(self, year, quarter, department):
        """Get the dictionary of courses from defined department from defined quarter.

        Args:
            year: the year of the requested quarter
            quarter: the requested quarter
            department: the name of the department we want to get courses from
        Returns:
            The dictionary of courses from defined department from defined quarter
        """
        coll = get_quarter_collections(year, quarter, "departments")
        department = coll.find({"deptName": department})
        if department.count() == 0:
            abort(404, message="Not Found(404): Department {0} doesn't exist in quarter {1} {2}".format(collection_name, year, quarter))
        department = json.loads(dumps(list(department)))
        courses = {course["UID"]:course for course in department[0]["courses"]}
        return courses

    def get(self):
        """The function that execute when receiving a courses get request.

        Args(from request body):
            year: the year of the requested quarter
            quarter: the requested quarter
            department(optional): the name of the department we want to get courses from
        Returns:
            The dictionary of courses from defined quarter

        """
        request.get_json()
        args = parser.parse_args()
        try:
            year = int(args['year'])
            quarter = str(args['quarter'])
            department = str(args['department'])
        except:
            abort_invalid_input("Invalid Input(400): Please check you input parameters!")
        if year and quarter:
            if department != 'None':
                return self.get_by_quarter_department(year, quarter, department)
            return self.get_by_quarter(year, quarter)

class departmentList(Resource):
    def get_by_quarter(self, year, quarter):
        """Get the list of departments from defined quarter.

        Args:
            year: the year of the requested quarter
            quarter: the requested quarter
        Returns:
            The list of departments from defined quarter

        """
        coll = get_quarter_collections(year, quarter, "departments")
        departments = coll.find()
        departments = json.loads(dumps(list(departments)))
        departments = [department["deptName"] for department in departments]
        return departments

    def get(self):
        """The function that execute when receiving a departments get request.

        Args(from request body):
            year: the year of the requested quarter
            quarter: the requested quarter
        Returns:
            The list of departments from defined quarter

        """
        request.get_json()
        args = parser.parse_args()
        try:
            year = int(args['year'])
            quarter = str(args['quarter'])
        except:
            abort_invalid_input("Invalid Input(400): Please check you input parameters!")
        if year and quarter:
            return self.get_by_quarter(year, quarter)

api.add_resource(departmentList, '/departments')
api.add_resource(courseList, '/courses')
api.add_resource(course, '/course')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)