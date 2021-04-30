import sys, json
sys.path.append('..')
from app import *
from src.util import *
from flask import Flask, abort, request, jsonify, render_template
from flask_restful import reqparse, abort, Api, Resource
from bson.json_util import dumps, loads

parser = reqparse.RequestParser()
parser.add_argument('year')
parser.add_argument('quarter')
parser.add_argument('department')

class DepartmentList(Resource):
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