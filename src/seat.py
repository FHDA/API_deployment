import sys, json

sys.path.append("..")
from app import *
from src.util import *
from flask import Flask, abort, request, jsonify, render_template
from flask_restful import reqparse, abort, Api, Resource
from bson.json_util import dumps, loads

parser = reqparse.RequestParser()
parser.add_argument("year")
parser.add_argument("quarter")
parser.add_argument("course_id")


class Seat(Resource):
    def get_by_quarter(self, year, quarter, course_id):
        """Get the enrollment data with defined course_id from defined quarter.

        Args:
            year: the year of the requested quarter
            quarter: the requested quarter
            course_id: the crn of the course requested
        Returns:
            The enrollment data with defined course_id from defined quarter

        """
        coll = get_quarter_collections(year, quarter, "seats")
        courses = coll.find({"UID": course_id})
        courses = json.loads(dumps(list(courses)))
        courses = {course["UID"]: course for course in courses}
        abort_if_course_doesnt_exist(course_id, courses, year, quarter)
        return courses[course_id]

    def get(self):
        """The function that execute when receiving a seat get request.

        Args(from request body):
            year: the year of the requested quarter
            quarter: the requested quarter
            course_id: the crn of the course requested
        Returns:
            The enrollment data with defined course_id from defined quarter

        """
        request.get_json()
        args = parser.parse_args()
        try:
            year = int(args["year"])
            quarter = str(args["quarter"])
            course_id = str(args["course_id"])
        except:
            abort_invalid_input(
                "Invalid Input(400): Please check you input parameters!"
            )
        if year and quarter != "None" and course_id != "None":
            return self.get_by_quarter(year, quarter, course_id)
        else:
            abort_invalid_input(
                "Invalid Input(400): Please provide all parameters to proceed!"
            )


class SeatList(Resource):
    def get_by_quarter(self, year, quarter):
        """Get the dictionary of enrollment data from defined quarter.

        Args:
            year: the year of the requested quarter
            quarter: the requested quarter
        Returns:
            The dictionary of enrollment data from defined quarter

        """
        coll = get_quarter_collections(year, quarter, "seats")
        courses = coll.find()
        courses = json.loads(dumps(list(courses)))
        courses = {course["UID"]: course for course in courses}
        return courses

    def get(self):
        """The function that execute when receiving a seats get request.

        Args(from request body):
            year: the year of the requested quarter
            quarter: the requested quarter
        Returns:
            The dictionary of courses from defined quarter

        """
        request.get_json()
        args = parser.parse_args()
        try:
            year = int(args["year"])
            quarter = str(args["quarter"])
        except:
            abort_invalid_input(
                "Invalid Input(400): Please check you input parameters!"
            )
        if year and quarter:
            return self.get_by_quarter(year, quarter)
