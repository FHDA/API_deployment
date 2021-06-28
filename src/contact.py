import sys, json

sys.path.append("..")
from app import *
from src.util import *
from datetime import datetime
from flask import Flask, abort, request, jsonify, render_template
from flask_restful import reqparse, abort, Api, Resource
from bson.json_util import dumps, loads

MILLISECOND_ELIMINATOR = -7

parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("email")
parser.add_argument("form_body")


class ContactForm(Resource):
    def get_by_email(self, email):
        """Get the forms with defined email address.

        Args:
            email: the email address to find contact form
        Returns:
            The list of forms sent by this email address

        """
        db = get_db("contact_forms")
        coll = db.get_collection("contact_test")
        forms = list(coll.find({"email": email}))
        if len(forms) == 0:
            abort_if_email_doesnt_exist(email, forms)
        forms = json.loads(dumps(forms))
        forms = {form["time"]: form for form in forms}
        return forms

    def get_by_oid(self, oid):
        """Get the forms with defined email address.

        Args:
            oid: the oid address to find contact form
        Returns:
            The list of forms sent by this email address

        """
        db = get_db("contact_forms")
        coll = db.get_collection("contact_test")
        forms = list(coll.find({"_id": oid}))
        if len(forms) == 0:
            abort_not_found("Contact Form Upload Failed!")
        return forms[0]

    def get(self):
        """The function that execute when receiving a contact form get request.

        Args(from request body):
            email: the email address from sender of the contact form
        Returns:
            The course with defined course_id from defined quarter

        """
        request.get_json()
        args = parser.parse_args()
        try:
            name = str(args["name"])
            email = str(args["email"])
            formBody = str(args["form_body"])
        except:
            abort_invalid_input(
                "Invalid Input(400): Please check you input parameters!"
            )
        if email != "None":
            return self.get_by_email(email)
        else:
            abort_invalid_input(
                "Invalid Input(400): Please provide all parameters to proceed!"
            )

    def post(self):
        """The function that execute when receiving a contact form post request.

        Args(from request body):
            email: the email address from sender of the contact form
            name: the name of the sender of the contact form
            form_body: the content of the form
        Returns:
            The uploaded object id and the corresponding HTTP return code

        """
        request.get_json()
        args = parser.parse_args()
        print(args)
        try:
            name = str(args["name"])
            email = str(args["email"])
            formBody = str(args["form_body"])
        except:
            abort_invalid_input(
                "Invalid Input(400): Please check you input parameters!"
            )
        if email != "None" and name != "None" and formBody != "None":
            time = str(datetime.now())[:MILLISECOND_ELIMINATOR]
            uploadBody = {
                "time": time,
                "name": name,
                "email": email,
                "form_body": formBody,
                "assigned": False,
                "assigned_to": "",
                "replied": False,
            }
            db = get_db("contact_forms")
            coll = db.get_collection("contact_test")
            oid = coll.insert_one(uploadBody).inserted_id
            postCheck = self.get_by_oid(oid)
            del postCheck["_id"]
            return postCheck, 201

        else:
            abort_invalid_input(
                "Invalid Input(400): Please provide all parameters to proceed!"
            )
