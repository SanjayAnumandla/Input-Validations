import re
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def is_valid_name(name):
    # Regex for name validation
    pattern = r"^(?:(?:[A-Za-z]+|([A-Za-z]+[-'][A-Za-z]+))(?:\s|$)){1,3}$"
    return bool(re.match(pattern, name))

def is_valid_phone(phone_number):
    # Regex for phone number validation
    pattern = r"^(\+?(\d{1,3})?[-. ]?)?(\()?(\d{2,4})(\))?[-. ]?(\d{2,4}[-. ]?){2}\d{2,4}|(\d{5}[-. ]\d{5})$"
    return bool(re.match(pattern, phone_number))


def write_audit_log(action, name=None):
    with open(config["Phonebook"]["AuditLog"], "a") as f:
        if name:
            f.write(f"{action}: {name}\n")
        else:
            f.write(f"{action}\n")
