from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, redirect, request
import re
from unittest import result
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = 'recipe_db'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s);"
        result = connectToMySQL(db).query_db(query, data)
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        return result

    @classmethod
    def get_email(cls, user):
        query = "SELECT * from users where email = %(email)s;"
        user = connectToMySQL(db).query_db(query, user)
        if not user:
            return False
        else:
            return cls(user[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * from users where id = %(id)s;"
        user = connectToMySQL(db).query_db(query, data)
        if not user:
            return False
        else:
            return cls(user[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("Please type your full name.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Please type your full name.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Please type a valid email address.")
            is_valid = False
        if User.get_email({'email': user['email']}):
            flash("An account with this email already exists.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Your password must be at least 8 characters.")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid
