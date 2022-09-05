import queue
from unittest import result
from flask import flash
import re

from flask_app.config.mysqlconnection import connectToMySQL
db = 'email_db'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO emails (email) VALUES (%(email)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_all_emails(cls):
        query = "SELECT * FROM emails;"
        result = connectToMySQL(db).query_db(query)
        emails = []
        for user in result:
            emails.append(cls(user))
        return emails

    @classmethod
    def get_one_email(cls, data):
        query = "SELECT * from emails where email = (%(email)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @staticmethod
    def validate(user):
        is_valid = True
        if len(user['email']) < 3:
            flash("Please enter a valid email address")
            is_valid = False
        if User.get_one_email({'email': user['email']}):
            flash("This email is already in use.")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Please enter a valid email address.")
            is_valid = False
        return is_valid
