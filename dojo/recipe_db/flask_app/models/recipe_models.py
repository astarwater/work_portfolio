from cgitb import reset
import re
from flask import flash, redirect, request, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
db = 'recipe_db'


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.time = data['time']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.date = data['date']
        self.users_id = data['users_id']

    @classmethod
    def submit_recipe(cls, data):
        query = "INSERT INTO recipes (name, time, description, instructions, users_id) VALUES (%(name)s, %(time)s, %(description)s, %(instructions)s, %(users_id)s);"
        result = connectToMySQL(db).query_db(query, data)
        # print(result)
        return result

    @classmethod
    def display_recipes(cls):
        query = "SELECT * from recipes;"
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def display_one_recipe(cls, data):
        query = "SELECT * from recipes WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes where id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, time=%(time)s, description=%(description)s, instructions=%(instructions)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if recipe.get('name') is None:
            flash("Please enter a name.")
            is_valid = False
        if len(recipe['name']) < 3:
            flash("Recipe name must be at least 3 characters.")
            is_valid = False
        # if recipe.get('date') is None:
        #     flash("Please enter the date for when this recipe was created.")
        #     is_valid = False
        if recipe.get('time') is None:
            flash("Please specify how long this recipe takes.")
            is_valid = False
        if recipe.get('description') is None:
            flash("Please enter a description.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if recipe.get('instructions') is None:
            flash("Please enter instructions.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        return is_valid
