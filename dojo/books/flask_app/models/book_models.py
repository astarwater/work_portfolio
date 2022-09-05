from cgitb import reset
from multiprocessing import AuthenticationError
import re
from flask import flash, redirect, request, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author_models
db = 'books_and_authors_db'

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_authors = []

    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(db).query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books

    @classmethod
    def get_one_b(cls, data):
        query = "SELECT * FROM books where title = (%(title)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def new_book(cls, data):
        query = "INSERT into books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_one_book(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.books_id LEFT JOIN authors on authors.id = favorites.authors_id where books.id = (%(id)s);"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) == 0:
            return False
        else:
            book = cls(results[0])
            for row in results:
                author = {
                    'id':row['authors.id'],
                    'name':row['name'],
                    'created_at':row['created_at'],
                    'updated_at':row['updated_at']
                }
                author = author_models.Author(author)
                book.favorite_authors.append(author)
            return book

    @classmethod
    def favorite_author(cls, data):
        query = "INSERT INTO favorites (books_id, authors_id) VALUES (%(book_id)s, %(author_id)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @staticmethod
    def validate(book):
        is_valid = True
        if len(book['title']) < 3:
            flash("Please enter 3 or more letters")
            is_valid = False
        if Book.get_one_b({'title': book['title']}):
            flash("Book has already been added!")
            is_valid = False
        return is_valid
