import sys, json

sys.path.append("..")
from app import *
from src.util import *
from flask import Flask, abort, request, jsonify, render_template
from flask_restful import reqparse, abort, Api, Resource
from bson.json_util import dumps, loads

parser = reqparse.RequestParser()
parser.add_argument("tag")
parser.add_argument("display")


class Hashtag(Resource):
    def get(self):
        """Gets the hastag list.

        Returns:
            A list of hashtag details

        Example:
        [
            {
                "name": "example_tag_1",
                "is_display": 1
            },
            {
                "name": "example_tag_2",
                "is_display": 1
            },
            {
                "name": "example_tag_3",
                "is_display": 0
            }
        ]
        """
        request.get_json()
        args = parser.parse_args()
        print(args)
        if args["display"] and args["tag"]:
            abort_invalid_input(
                "Invalid Input(400): Please check you input parameters!"
            )
        db = get_db(db_name="miscellaneous")
        coll = db["hashtag"]
        if args["tag"]:
            cursor = coll.find({"name": str(args["tag"])})
        elif args["display"]:
            cursor = coll.find({"is_display": str(args["display"])})
        else:
            cursor = coll.find()
        res = []
        for tag in cursor:
            res.append({"name": tag["name"], "is_display": tag["is_display"]})
        return res

    def post(self):
        """Adds a tag into hashtag list.

        Args(from request body):
            tag: tag name
            display: display status (default 1)
        Returns:
            Post result or error
        """
        request.get_json()
        args = parser.parse_args()
        try:
            tag = str(args["tag"])
            if "display" not in args:
                is_display = 1
            else:
                is_display = int(args["display"])
        except:
            abort_invalid_input(
                "Invalid Input(400): Please check you input parameters!"
            )
        db = get_db(db_name="miscellaneous")
        coll = db["hashtag"]
        try:
            insert_tag = {"name": tag, "is_display": is_display}
            if coll.find_one({"name": tag}):
                abort_invalid_input(
                    "Invalid Input(400): Cannot insert tag already in DB"
                )
            result = coll.update_one(
                filter={"name": tag}, update={"$set": insert_tag}, upsert=True
            )
        except Exception as e:
            abort_not_found(str(e))
        return (
            str(result.upserted_id)
            if result.upserted_id
            else "400, Unable to POST to MongoDB"
        )

    def put(self):
        """Updates a tag into hashtag list.

        Args(from request body):
            tag: tag name
            display: display status
        Returns:
            PUT result
        """
        request.get_json()
        args = parser.parse_args()
        try:
            tag = str(args["tag"])
            is_display = int(args["display"])
        except:
            abort_invalid_input(
                "Invalid Input(400): Please check you input parameters!"
            )
        db = get_db(db_name="miscellaneous")
        coll = db["hashtag"]
        try:
            update_tag = {"name": tag, "is_display": is_display}
            result = coll.update_one(
                filter={"name": tag}, update={"$set": update_tag}, upsert=False
            )
        except Exception as e:
            abort_not_found(str(e))
        if result.modified_count > 0:
            return "200, Successful"
        elif result.upserted_id != None:
            return "200, Inserted new tag"
        else:
            return "400, Did not update"

    def delete(self):
        """Deletes a tag from hashtag list.

        Args(from request body):
            tag: tag name
        Returns:
            Post result or error
        """
        request.get_json()
        args = parser.parse_args()
        try:
            tag = str(args["tag"])
        except:
            abort_invalid_input(
                "Invalid Input(400): Please check you input parameters!"
            )
        db = get_db(db_name="miscellaneous")
        coll = db["hashtag"]
        try:
            result = coll.delete_one({"name": tag})
        except Exception as e:
            abort_not_found(str(e))
        return "Success" if result.deleted_count == 1 else "Unable to delete!"
