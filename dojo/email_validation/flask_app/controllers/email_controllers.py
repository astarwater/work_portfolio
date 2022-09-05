from crypt import methods
from unittest import result
from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.email_model import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def validate():
    if not User.validate(request.form):
        return redirect('/')
    data = {
        'email': request.form['email']
    }
    User.save(data)
    return render_template('show_emails.html', users=User.get_all_emails())
