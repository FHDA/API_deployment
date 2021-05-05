# -*- coding: utf-8 -*-
"""API component.

This module gets request from frontend and make corresponding responses
"""
from src.course import Course, CourseList
from src.department import Department, DepartmentList
from src.seat import Seat, SeatList
from flask import Flask, abort, request, jsonify, render_template
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
api.add_resource(Department, '/department')
api.add_resource(DepartmentList, '/department_list')
api.add_resource(Course, '/course')
api.add_resource(CourseList, '/course_list')
api.add_resource(SeatList, '/seat_list')
api.add_resource(Seat, '/seat')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)