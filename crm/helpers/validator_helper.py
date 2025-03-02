import re
from datetime import datetime
from crm.models.clients import Client
from crm.models.collaborators import Collaborator
from crm.models.contracts import Contract
from crm.models.roles import Role, RoleEnum
from crm.enums.model_type_enum import ModelTypeEnum
from crm.enums.foreign_key_type_enum import ForeignKeyTypeEnum
from config import SECRET_KEY, KEYRING_SERVICE

class ValidatorHelper:
    def __init__(self, context, model_type, data):
        self.context = context
        self.model_type = model_type
        self.data = data
        self.error_messages = []
        
        self.client_required_fields = ["first_name", "last_name", "email", "phone", "company_name"]
        self.client_valid_fields = self.client_required_fields + ["first_contact_date", "last_contact_date", "commercial_id"]
        
        self.collaborator_required_fields = ["first_name", "last_name", "email", "password", "role_id"]
        self.collaborator_valid_fields = self.collaborator_required_fields
        
        self.contract_required_fields = ["costing", "remaining_due_payment", "client_id", "commercial_id"]
        self.contract_valid_fields = self.contract_required_fields + ["is_signed"]
        
        self.event_required_fields = ["name", "start_date", "end_date", "location", "attendees", "contract_id"]
        self.event_valid_fields = self.event_required_fields + ["notes", "support_id"]

    def shortened_validate_data(self, field_name, type, func, min=None, max=None, foreign_key_type_enum=None):
        if field_name in self.data and self.data[field_name] and self.type_check(type, field_name, self.data[field_name]):
            if min is not None and max is not None:
                func(field_name, self.data[field_name], min, max)
            elif foreign_key_type_enum is not None:
                func(field_name, self.data[field_name], foreign_key_type_enum)
            else:
                func(field_name, self.data[field_name])

    def validate_data(self):
        """Validates data based on the model type"""
        if self.model_type == ModelTypeEnum.CLIENT:
            self.shortened_validate_data("first_name", str, self.validate_string, 0, 30)
            self.shortened_validate_data("last_name", str, self.validate_string, 0, 30)
            self.shortened_validate_data("email", str, self.validate_email)
            self.shortened_validate_data("phone", str, self.validate_phone_number)
            self.shortened_validate_data("company_name", str, self.validate_string, 0, 50)
            self.shortened_validate_data("first_contact_date", str, self.validate_datetime)
            self.shortened_validate_data("last_contact_date", str, self.validate_datetime)
            self.shortened_validate_data("commercial_id", int, self.validate_foreign_id, None, None, ForeignKeyTypeEnum.COMMERCIAL)

        elif self.model_type == ModelTypeEnum.COLLABORATOR:
            self.shortened_validate_data("first_name", str, self.validate_string, 0, 30)
            self.shortened_validate_data("last_name", str, self.validate_string, 0, 30)
            self.shortened_validate_data("email", str, self.validate_email)
            self.shortened_validate_data("password", str, self.validate_password)
            self.shortened_validate_data("role_id", int, self.validate_foreign_id, None, None, ForeignKeyTypeEnum.ROLE)

        elif self.model_type == ModelTypeEnum.CONTRACT:
            self.shortened_validate_data("costing", float, self.validate_number, 0)
            self.shortened_validate_data("remaining_due_payment", float, self.validate_number, 0)
            if self.data.get("is_signed"):
                self.type_check(bool, "is_signed", self.data["is_signed"])
            self.shortened_validate_data("client_id", int, self.validate_foreign_id, None, None, ForeignKeyTypeEnum.CLIENT)
            self.shortened_validate_data("commercial_id", int, self.validate_foreign_id, None, None, ForeignKeyTypeEnum.COMMERCIAL)

        elif self.model_type == ModelTypeEnum.EVENT:
            self.shortened_validate_data("name", str, self.validate_string, 0, 50)
            self.shortened_validate_data("start_date", str, self.validate_datetime)
            self.shortened_validate_data("end_date", str, self.validate_datetime)
            self.shortened_validate_data("location", str, self.validate_address)
            self.shortened_validate_data("attendees", int, self.validate_number, 0)
            self.shortened_validate_data("notes", str, self.validate_string, 0, 100000)
            self.shortened_validate_data("contract_id", int, self.validate_foreign_id, None, None, ForeignKeyTypeEnum.CONTRACT)
            self.shortened_validate_data("support_id", int, self.validate_foreign_id, None, None, ForeignKeyTypeEnum.SUPPORT)

        else:
            print("Invalid model type passed")

    def validate_email(self, field, value):
        self.validate_string(field, value, min_length=0, max_length=30)
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, value):
            self.add_error(field, "Invalid email format.")

    def validate_datetime(self, field, value):
        self.validate_string(field, value, min_length=0, max_length=20)
        try:
            datetime.strptime(value.strip(), "%d/%m/%Y-%Hh%M")
        except ValueError:
            self.add_error(field, "Invalid datetime format. Expected format: DD/MM/YYYY-HHhMM")

    def validate_string(self, field, value, min_length=0, max_length=None):
        if len(value) < min_length:
            self.add_error(field, f"Value must be at least {min_length} characters long.")
        if max_length is not None and len(value) > max_length:
            self.add_error(field, f"Value must not exceed {max_length} characters.")

    def validate_password(self, field, value):
        self.validate_string(field, value, min_length=0, max_length=40)
        if len(value) < 8:
            self.add_error(field, "Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            self.add_error(field, "Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            self.add_error(field, "Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            self.add_error(field, "Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            self.add_error(field, "Password must contain at least one special character.")

    def validate_number(self, field, value, min_value=0, max_value=None):
        if value < min_value:
            self.add_error(field, f"Value must be at least {min_value}.")
        if max_value is not None and value > max_value:
            self.add_error(field, f"Value must not exceed {max_value}.")

    def validate_phone_number(self, field, value):
        self.validate_string(field, value, min_length=0, max_length=20)
        phone_regex = r"^(\+?[0-9]{1,4}[\s\-]?)?(\(?[0-9]{1,5}\)?[\s\-]?[0-9]{1,5}[\s\-]?[0-9]{1,5})+$"
        if not re.match(phone_regex, value):
            self.add_error(field, "Invalid phone number format. Expected formats include '+44 20 7946 0958' (UK), '+33 1 70 18 99 87' (France), or '(030) 12345678' (Germany)")

    def validate_address(self, field, value):
        self.validate_string(field, value, min_length=0, max_length=100)
        address_regex = r"^\d+\s+[-\w\s]+,\s+\d+\s+[-\w\s]+,\s+[-\w\s-]+$"
        if not re.match(address_regex, value):
            self.add_error(
                field,
                "Invalid address format. Expected format: '<Street number> <Street name>, <City postal code>, <Country>'."
            )

    def validate_foreign_id(self, field, value, foreign_key_type_enum):
        """Check if foreign key exists in the database"""
        self.validate_number(field, value, 0)
        if foreign_key_type_enum == ForeignKeyTypeEnum.CLIENT:
            self.entity_exists_check(field, value, Client)
            
        elif foreign_key_type_enum == ForeignKeyTypeEnum.COMMERCIAL:
            self.entity_exists_check(field, value, Collaborator, RoleEnum.SALES)
                        
        elif foreign_key_type_enum == ForeignKeyTypeEnum.CONTRACT:
            self.entity_exists_check(field, value, Contract)
            
        elif foreign_key_type_enum == ForeignKeyTypeEnum.ROLE:
            self.entity_exists_check(field, value, Role)
            
        elif foreign_key_type_enum == ForeignKeyTypeEnum.SUPPORT:
            self.entity_exists_check(field, value, Collaborator, RoleEnum.SUPPORT)
        else:
            self.add_error(field, "Invalid foreign key")
            
    def entity_exists_check(self, field, entity_id, model, role_type_enum=None):
        entity = self.context.get(model, entity_id)
        if entity:
            if role_type_enum is not None and role_type_enum.value != entity.role_id:
                self.add_error(field, "The given collaborator is not of the authorized role")
                
            if model is Contract and not entity.is_signed:
                self.add_error(field, "It is not allowed to create an event for an unsigned contract")

        else:
            self.add_error(field, "No such entry registered in the database")

    def add_error(self, field, message):
        self.error_messages.append(f"{field}: {message}")

    def is_valid(self):
        return len(self.error_messages) == 0

    def type_check(self, expected_type, field, value):
        if not isinstance(value, expected_type):
            self.add_error(field, f"Expected type {expected_type.__name__}, got {type(value).__name__}.")
            return False
        return True
