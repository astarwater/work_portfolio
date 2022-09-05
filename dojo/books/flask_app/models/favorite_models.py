# from cgitb import reset
# import re
# from unittest import result
# from flask import flash, redirect, request, session
# from flask_app import app
# from flask_app.config.mysqlconnection import connectToMySQL
# db = 'books_and_authors_db'

# class Favorite:
#     def __init__(self, data):
#         self.authors_id = data['authors_id']
#         self.books_id = data['books_id']
#         self.created_at = data['created_at']
#         self.updated_at = data['updated_at']

#     @classmethod
#     def show_favorites(cls, data):
#         query = "SELECT * FROM favorites WHERE authors_id = %(id)s;"
#         results = connectToMySQL(db).query_db(query, data)
#         return results

#     @classmethod
#     def add_favorite(cls, data):
#         query = "INSERT INTO favorites (authors_id) VALUES %(authors_id)s WHERE books_id = %(id)s;"
#         results = connectToMySQL(db).query_db(query, data)
#         return results