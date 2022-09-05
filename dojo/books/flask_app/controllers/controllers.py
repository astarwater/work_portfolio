import pwd
from tkinter.messagebox import RETRY
from flask import flash
from crypt import methods
from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.author_models import Author
from flask_app.models.book_models import Book

@app.route('/')
def index():
    authors = Author.get_all_authors()
    return render_template('index.html', authors=authors)

@app.route('/new_book')
def new_book():
    books = Book.get_all_books()
    return render_template('new_book.html', books = books)

@app.route('/home')
def home():
    return redirect('/')

@app.route('/add_book', methods=['POST'])
def add_book():
    if not Book.validate(request.form):
        return redirect('/new_book')
    Book.new_book(request.form)
    return redirect('/new_book')

@app.route('/new_author', methods= ['POST'])
def new_author():
    if not Author.validate(request.form):
        return redirect('/')
    Author.new_author(request.form)
    return redirect('/')

@app.route('/view/<int:author_id>')
def view_author(author_id):
    data = {
        'id': author_id
    }
    session['author_id'] = author_id
    author = Author.get_one(data)
    books = Book.get_all_books()
    return render_template('author_show.html', author=author, books=books)

@app.route('/add_favorite_book', methods=['POST'])
def add_favorite():
    data = {
        'book_id':request.form['favorite_book'],
        'author_id':session['author_id']
    }
    Author.favorite_book(data)
    author_id = session['author_id']
    return redirect(f'/view/{author_id}')

@app.route('/view_book/<int:book_id>')
def view_book(book_id):
    data = {
        'id': book_id
    }
    session['book_id'] = book_id
    authors = Author.get_all_authors()
    book = Book.get_one_book(data)
    return render_template('book_show.html', authors=authors, book=book)

@app.route('/add_favorite_author', methods=['POST'])
def add_favorite_author():
    data = {
        'author_id':request.form['author_fav'],
        'book_id':session['book_id']
    }
    Book.favorite_author(data)
    book_id = session['book_id']
    return redirect(f'/view_book/{book_id}')

