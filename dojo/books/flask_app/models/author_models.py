from cgitb import reset
import re
from unittest import result
from flask import flash, redirect, request, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book_models
db = 'books_and_authors_db'

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []

    @classmethod
    def new_author(cls, data):
        query = "INSERT into authors (name) VALUES (%(name)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL(db).query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors

    @classmethod
    def get_one_author(cls, data):
        query = "SELECT * FROM authors where name = (%(name)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.authors_id LEFT JOIN books ON books.id = favorites.books_id where authors.id = (%(id)s);"
        results = connectToMySQL(db).query_db(query,data)
        if results == 0:
            return False
        else:
            author = cls(results[0])
            for row in results:
                book = {
                    'id':row['books.id'],
                    'title':row['title'],
                    'num_of_pages':row['num_of_pages'],
                    'created_at':row['books.created_at'],
                    'updated_at':row['books.updated_at']
                }
                book = book_models.Book(book)
                author.favorite_books.append(book)
            return author

    @classmethod
    def favorite_book(cls, data):
        query = "INSERT INTO favorites (books_id, authors_id) VALUES (%(book_id)s, %(author_id)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result
    
    @staticmethod
    def validate(author):
        is_valid = True
        if len(author['name']) < 3:
            flash("Please enter 3 or more letters.")
            is_valid = False
        if Author.get_one_author({'name': author['name']}):
            flash("Author has already been added!")
            is_valid = False
        return is_valid
    