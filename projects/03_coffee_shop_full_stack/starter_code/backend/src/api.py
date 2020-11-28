import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

# removed a period from the start of database.models. Or not.
from .database.models import db_drop_and_create_all, setup_db, Drink
# removed a period from the start of auth.auth. Or not.
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_drinks():
    try:
        db_drinks = Drink.query.all()
    except Exception:
        abort(404)
    drinks = [drink.short() for drink in db_drinks]
    response = jsonify({'success': True, 'drinks': drinks})
    return response


@requires_auth('get:drinks-detail')
@app.route('/drinks-detail')
def get_drinks_with_detail():
    db_drinks = Drink.query.all()
    drinks = [d.long() for d in db_drinks]
    response = jsonify({'success': True, 'drinks': drinks})
    return response


@requires_auth('post:drinks')
@app.route('/drinks', methods=['POST'])
def create_drink():
    data = json.loads(request.data)
    id = data.get('id', None)
    title = data.get('title', None)
    recipe = data.get('recipe', None)

    try:
        new_drink = Drink(title=title, recipe=recipe)
        new_drink.insert()
    except Exception as e:
        print('There was an exception:')
        print(e)
        abort(422)

    response = jsonify({'success': True, 'drinks': [new_drink.long()]})
    return response


@requires_auth('patch:drinks')
@app.route('/drinks/<int:id>', methods=['PATCH'])
def edit_drink(id):
    try:
        db_drink = Drink.query.get(id)
    except Exception:
        abort(404)

    data = json.loads(request.data)
    title = data.get('title', None)
    recipe = data.get('recipe', None)

    try:
        if title:
            db_drink.title = title
        if recipe:
            db_drink.recipe = recipe
        db_drink.update()
    except Exception as e:
        print('There was an exception:')
        print(e)
        abort(422)

    response = jsonify({'success': True, 'drinks': [db_drink.long()]})
    return response


@requires_auth('delete:drinks')
@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drink(id):
    try:
        db_drink = Drink.query.get(id)
    except Exception:
        abort(404)

    try:
        db_drink.delete()
    except Exception as e:
        print('There was an exception:')
        print(e)
        abort(401)

    response = jsonify({'success': True, 'delete': id})
    return response


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "user is not authorized to access this resource"
    }), 401
