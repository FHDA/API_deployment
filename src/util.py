import os
from flask import Flask, abort, request, jsonify, render_template
from flask_restful import reqparse, abort, Api, Resource
from configparser import ConfigParser
from pymongo import MongoClient
from pymongo import errors as mongoerrors

def get_db():
    """Get MongoDB username and password from the config file and return the desired database.

    Raises:
        pymongo.errors: possibly connection errors or conficuration errors
    Returns:
        The database object

    """
    env_config = ConfigParser()
    env_config.read(os.path.dirname(os.path.abspath(__file__))+'/../config/setting.config')
    mongo_config = env_config['MongoDB']
    username, password = mongo_config['Mongo_User'], mongo_config['Mongo_Password']
    db_name = mongo_config['Mongo_DBName']
    client = MongoClient('mongodb+srv://' + username + ':' + password+ mongo_config['Mongo_Postfix'])
    return client.get_database(db_name)

def get_quarter_collections(year, quarter, collection_type):
    """Get the collection from db according to defined quarter and the type of collection requested.

    Args:
        year: the year of the requested quarter
        quarter: the requested quarter
        collection_type: str, either "courses" or "departments"
    Returns:
        The collection received from db

    """
    db = get_db()
    collection_name = str(year) + " " + quarter + " De Anza " + collection_type
    coll = db.get_collection(collection_name)
    if coll.count() == 0:
        abort(404, message="Not Found(404): Database collection entry {} doesn't exist".format(collection_name))
    return coll

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

def abort_if_department_doesnt_exist(department, departments, year=None, quarter=None):
    """Send error message if department does not exist.

    Send corresponding error message if a requested department does not exist

    Args:
        department: the name of the department requested
        departments: the dictionary of departments loaded from db
        year: the year of the requested quarter
        quarter: the requested quarter
    Returns:
        None

    """
    if department not in departments:
        if year and quarter:
            abort(404, message="Not Found(404): Department {0} doesn't exist in quarter {1} {2}".format(department, year, quarter))
        else:
            abort(404, message="Not Found(404): Department {} doesn't exist".format(department))

def abort_invalid_input(err_message):
    """Send an error message 400.
    """
    abort(400, message=err_message)

def abort_not_found(err_message):
    """Send an error message 404.
    """
    abort(404, message=err_message)