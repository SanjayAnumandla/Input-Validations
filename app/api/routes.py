from flask import request
from flask_restful import Resource, Api
from app import create_app, db
from app.models import Phonebook
from app.validators import is_valid_name, is_valid_phone, write_audit_log

app = create_app()
api = Api(app)

class PhonebookResource(Resource):
    def get(self, name):
        if not is_valid_name(name):
            return {"message": "Invalid name format"}, 400

        contact = Phonebook.query.filter_by(name=name).first()

        if contact:
            return {"name": contact.name, "phone_number": contact.phone_number}
        else:
            return {"message": "Contact not found"}, 404

    def put(self, name):
        if not is_valid_name(name):
            return {"message": "Invalid name format"}, 400

        phone_number = request.form.get('phone_number')

        if not is_valid_phone(phone_number):
            return {"message": "Invalid phone number format"}, 400

        contact = Phonebook.query.filter_by(name=name).first()

        if contact:
            contact.phone_number = phone_number
            db.session.commit()
            write_audit_log("Updated", name)
            return {"message": "Contact updated successfully"}
        else:
            new_contact = Phonebook(name=name, phone_number=phone_number)
            db.session.add(new_contact)
            db.session.commit()
            write_audit_log("Added", name)
            return {"message": "Contact added successfully"}

    def delete(self, name):
        if not is_valid_name(name):
            return {"message": "Invalid name format"}, 400

        contact = Phonebook.query.filter_by(name=name).first()

        if contact:
            db.session.delete(contact)
            db.session.commit()
            write_audit_log("Deleted", name)
            return {"message": "Contact deleted successfully"}
        else:
            return {"message": "Contact not found"}, 404

api.add_resource(PhonebookResource, '/phonebook/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
