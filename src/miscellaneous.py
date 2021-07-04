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

        Args(from request body):
            tag: tag name
            display: display status (default 1)
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
        if args["display"] and args["tag"]:
            return generate_response("Please check you input parameters!", 400)
        db = get_db(db_name="miscellaneous")
        coll = db["hashtag"]
        if args["tag"]:
            cursor = coll.find({"name": str(args["tag"])})
        elif args["display"]:
            cursor = coll.find({"is_display": int(args["display"])})
        else:
            cursor = coll.find()
        res = []
        for tag in cursor:
            res.append({"name": tag["name"], "is_display": tag["is_display"]})
        return (
            generate_response(res, 200)
            if res != []
            else generate_response("Specified tag is not found!", 404)
        )

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
            if not args["tag"]:
                raise Exception("Tag name is not in argument list")
            tag = str(args["tag"])
            if not args["display"]:
                is_display = 1
            else:
                is_display = int(args["display"])
        except:
            return generate_response("Please check you iput parameters!", 400)
        db = get_db(db_name="miscellaneous")
        coll = db["hashtag"]
        try:
            insert_tag = {"name": tag, "is_display": is_display}
            if coll.find_one({"name": tag}):
                return generate_response("Cannot insert tag already in DB", 400)
            result = coll.update_one(
                filter={"name": tag}, update={"$set": insert_tag}, upsert=True
            )
        except Exception as e:
            return generate_response(str(e), 400)
        return (
            generate_response(str(result.upserted_id), 200)
            if result.upserted_id
            else generate_response("Unable to POST to MongoDB!", 400)
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
            return generate_response("Please check you input parameters!", 400)
        db = get_db(db_name="miscellaneous")
        coll = db["hashtag"]
        try:
            update_tag = {"name": tag, "is_display": is_display}
            result = coll.update_one(
                filter={"name": tag}, update={"$set": update_tag}, upsert=False
            )
        except Exception as e:
            return generate_response(str(e), 404)
        if result.modified_count > 0:
            return generate_response("Successful", 200)
        elif result.upserted_id != None:
            return generate_response(result.upserted_id, 201)
        else:
            return generate_response("Failed to update!", 400)

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
            return generate_response("Please check you input parameters!", 400)
        db = get_db(db_name="miscellaneous")
        coll = db["hashtag"]
        try:
            result = coll.delete_one({"name": tag})
        except Exception as e:
            return generate_response(str(e), 404)
        return (
            generate_response("Success", 200)
            if result.deleted_count == 1
            else generate_response("Unable to delete!", 404)
        )
