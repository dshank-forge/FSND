import json
import os
from flask import Flask, request, jsonify, abort, _request_ctx_stack
from flask_cors import CORS
from functools import wraps
from jose import jwt, exceptions
from sqlalchemy import exc
from urllib.request import urlopen

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import (AuthError, requires_auth, get_token_auth_header,
                        verify_decode_jwt, check_permissions)

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


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_with_detail():
    db_drinks = Drink.query.all()
    drinks = [d.long() for d in db_drinks]
    print(drinks)
    response = jsonify({'success': True, 'drinks': drinks})
    return response


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    try:
        data = json.loads(request.data)
    except Exception:
        abort(401)
    id = data.get('id', None)
    title = data.get('title', None)
    recipe = data.get('recipe', None)
    recipe_as_list = [recipe]
    recipe_as_list_as_string = '"' + str(recipe_as_list) + '"'

    try:
        new_drink = Drink(title=title, recipe=recipe_as_list_as_string)
        new_drink.insert()
    except Exception as e:
        print('There was an exception:')
        print(e)
        abort(422)

    response = jsonify({'success': True, 'drinks': [new_drink.long()]})
    return response


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(id):
    try:
        db_drink = Drink.query.get(id)
        db_drink.id
    except Exception:
        abort(401)

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


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
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
