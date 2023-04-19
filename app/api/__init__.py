from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from ..models import Person
from .. import db
from .validation import is_valid_name, is_valid_phone, write_audit_log

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# ... Resource classes ...

api.add_resource(PhoneBookList, '/PhoneBook/list')
api.add_resource(PhoneBookAdd, '/PhoneBook/add')
api.add_resource(PhoneBookDeleteByName, '/PhoneBook/deleteByName')
api.add_resource(PhoneBookDeleteByNumber, '/PhoneBook/deleteByNumber')
