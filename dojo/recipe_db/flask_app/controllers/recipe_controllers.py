import pwd
from tkinter.messagebox import RETRY
from crypt import methods
from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user_models import User
from flask_app.models.recipe_models import Recipe
import os
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

picFolder = os.path.join('static', 'assets')

app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/')
def index():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'kitchen.jpg')
    return render_template('index.html', user_image = pic1)


@app.route('/register', methods=['POST'])
def register():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password']
    }
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data['pw_hash'] = pw_hash
    valid = User.validate_user(data)
    if valid:
        user = User.save(data)
        session['user_id'] = user
        return redirect('/dashboard')
    if not User.validate_user(request.form):
        return redirect('/')
    User.save(request.form)
    return redirect('/')


@app.route('/user/success')
def success():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    return render_template('recipes.html', user=user)


@app.route('/login', methods=['POST'])
def login():
    user = User.get_email(request.form)
    if not user:
       flash("Invalid email or password.")
       return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
       flash("Invalid email or password.")
       return redirect('/')
    session['user_id'] = user.id
    recipes = Recipe.display_recipes()
    return render_template('recipes.html', user=user, recipes=recipes)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/create')
def create():
    return render_template('add.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    recipes = Recipe.display_recipes()
    return render_template('recipes.html', user=user, recipes=recipes)


@app.route('/new_recipe', methods=['POST'])
def submit_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/create')
    Recipe.submit_recipe(request.form)
    return redirect('/dashboard')


@app.route('/view_instructions/<int:recipe_id>')
def view_instructions(recipe_id):
    data = {
        'id': recipe_id
    }
    user = User.get_one({'id': session['user_id']})
    return render_template('instructions.html', user=user, recipe=Recipe.display_one_recipe(data))


@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):
    data = {
        'id': recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')


@app.route('/edit/<int:recipe_id>')
def edit(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.display_one_recipe(data)
    print(recipe.users_id)
    print(session['user_id'])
    if session['user_id'] != recipe.users_id:
        return redirect('/dashboard')
    return render_template('edit.html', recipe=recipe)


@app.route('/update', methods=['POST'])
def update():
    if not Recipe.validate_recipe(request.form):
        return redirect('/dashboard')
    Recipe.edit_recipe(request.form)
    return redirect('/dashboard')
