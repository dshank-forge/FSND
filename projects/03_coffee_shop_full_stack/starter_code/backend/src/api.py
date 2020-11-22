import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink # removed a period from the start of database.models. Or not.
from .auth.auth import AuthError, requires_auth # removed a period from the start of auth.auth. Or not.

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@DONE
'''
@app.route('/drinks')
def get_drinks():
    db_drinks = Drink.query.all()
    drinks = [d.short() for d in db_drinks]
    response = jsonify({'success': True, 'drinks': drinks})
    return response 

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
# require 'get:drinks-detail' permission
@app.route('/drinks-detail')
def get_drinks_with_detail():
    db_drinks = Drink.query.all()
    drinks = [d.long() for d in db_drinks]
    response = jsonify({'success': True, 'drinks': drinks})
    return response


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink is an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
# require 'post:drinks' permission
@app.route('/drinks', methods=['POST'])
def create_drink():
    data = json.loads(request.data)
    id = data.get('id', None)
    title = data.get('title', None)
    recipe = data.get('recipe', None)

    try:
        new_drink = Drink(title=title, recipe=recipe)
        new_drink.insert()
    except(ArithmeticError, AttributeError, LookupError, SyntaxError, ValueError) as e:
        print('There was an exception:')
        print(e)
        abort(422)

    response = jsonify({'success': True, 'drinks': [new_drink.long()]})
    return response 


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
# require 'patch:drinks' permission
@app.route('/drinks/<int:id>', methods=['PATCH'])
def edit_drink(id):
    try:
        db_drink = Drink.query.get(id)
    except:
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
    except(ArithmeticError, AttributeError, LookupError, SyntaxError, ValueError) as e:
        print('There was an exception:')
        print(e)
        abort(422)
    
    response = jsonify({'success': True, 'drinks': [db_drink.long()]})
    return response

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
# require 'delete:drinks' permission
@app.route('/drinks/<int:id>', methods='DELETE')
def delete_drink(id):
    pass



## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
