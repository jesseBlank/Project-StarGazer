from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Have import from mysqlconnection on every model for DB interactions
# Import the model's python file as a module, not the class directly so you avoid circular import errors!
# For example: from flask_app.models import table2_model

'''
! Note: If you are working with tables that are related to each other, 
!       you'll want to import the other table's class here for when you need to create objects with that class. 

! Example: importing pets so we can make pet objects for our users that own them.

Class should match the data table exactly that's in your DB.

REMEMBER TO PARSE DATA INTO OBJECTS BEFORE SENDING TO PAGES!

'''

class User:
    DB = 'space_schema'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(new_user):
        is_valid = True
        if len(new_user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(new_user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(new_user['email']):
            flash("Invalid email address.")
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email= %(email)s;"
            results = connectToMySQL(User.DB).query_db(query, new_user)
            if len(results) >= 1:
                flash('Email already in use!')
                is_valid = False
        if len(new_user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if new_user['password'] != new_user['confirm_password']:
            flash('Passwords did not match')
            is_valid = False
        return is_valid

    @classmethod
    def create_user(cls,data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def get_user_by_id(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(user_id)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])