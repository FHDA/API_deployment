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
parser.add_argument("department")
parser.add_argument("course_id")


class Course(Resource):
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
        courses = {course["UID"]: course for course in courses}
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
            year = int(args["year"])
            quarter = str(args["quarter"])
            department = str(args["department"])
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


class CourseList(Resource):
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
        courses = {course["UID"]: course for course in courses}
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
            abort(
                404,
                message="Not Found(404): Department {0} doesn't exist in quarter {1} {2}".format(
                    collection_name, year, quarter
                ),
            )
        department = json.loads(dumps(list(department)))
        courses = {course["UID"]: course for course in department[0]["courses"]}
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
            year = int(args["year"])
            quarter = str(args["quarter"])
            department = str(args["department"])
        except:
            abort_invalid_input(
                "Invalid Input(400): Please check you input parameters!"
            )
        if year and quarter:
            if department != "None":
                return self.get_by_quarter_department(year, quarter, department)
            return self.get_by_quarter(year, quarter)
