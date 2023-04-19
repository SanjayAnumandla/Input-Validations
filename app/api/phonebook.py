from flask import request
from flask_restful import Resource
from app.models import PhoneBook
from app.utils import is_valid_name, is_valid_phone, write_audit_log

class PhoneBookList(Resource):
    def get(self):
        write_audit_log("List")
        return PhoneBook.list()

class PhoneBookAdd(Resource):
    def post(self):
        name = request.json.get("name")
        phone_number = request.json.get("phone_number")

        if not (is_valid_name(name) and is_valid_phone(phone_number)):
            return {"error": "Invalid input"}, 400

        PhoneBook.add(name, phone_number)
        write_audit_log("Add", name)

        return {"result": "Person added"}, 200

class PhoneBookDeleteByName(Resource):
    def put(self):
        name = request.json.get("name")

        if not is_valid_name(name):
            return {"error": "Invalid name"}, 400

        if name not in PhoneBook.contacts:
            return {"error": "Name not found"}, 404

        PhoneBook.delete_by_name(name)
        write_audit_log("Remove", name)

        return {"result": "Person removed"}, 200

class PhoneBookDeleteByNumber(Resource):
    def put(self):
        phone_number = request.json.get("phone_number")

        if not is_valid_phone(phone_number):
            return {"error": "Invalid phone number"}, 400

        initial_count = len(PhoneBook.contacts)
        PhoneBook.delete_by_number(phone_number)

        if initial_count == len(PhoneBook.contacts):
            return {"error": "Phone number not found"}, 404

        write_audit_log("Remove", phone_number)

        return {"result": "Person removed"}, 200
