import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  cors = CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    categories = [c.type for c in categories]
    response = jsonify({'success' : True, 'categories' : categories})
    return response 

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_all_questions():
    questions = Question.query.all()
    questions = [q.question for q in questions]
    total_questions = len(questions)
    categories = Category.query.all()
    categories = [c.type for c in categories]
    #how do I get current category?
    #
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions_on_page = questions[start:end] 

    response = jsonify({
      'success' : True,
      'questions' : questions_on_page,
      'total_questions' : total_questions,
      'categories' : categories,
      'current_category' : 1
    })
    
    # test_result = {
    #   'success' : True,
    #   'questions' : ['q1', 'q2', 'q3'],
    #   'total_questions': 3,
    #   'categories' : ['c1', 'c2', 'c3'],
    #   'current_category' : 'c1'
    # }
    # return jsonify(test_result)  

    return response 


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    Q = Question.query.get(question_id)
    try:  
        Q.delete()
    except: 
        abort(422)

    return jsonify({'success':True})

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    data = json.loads(request.data)

    try:
        question = data['question']
    except KeyError:
        question = None
    try:
        answer = data['answer']
    except KeyError:
        answer = None
    try:
        difficulty = data['difficulty']
    except KeyError:
        difficulty = None
    try:
        category = data['category']
    except KeyError:
        category = None
    try:
        search_term = data['searchTerm']
    except KeyError:
        search_term = None

    # Search for questions
    if search_term:
        query_results = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
        questions = [{'question': q.question, 'answer': q.answer, 'category': q.category, 'difficulty': q.difficulty} for q in query_results]
        # query_results = Question.query.filter(Question.question.ilike('%o%')).all()
        total_questions = len(query_results)
        have_results = bool(total_questions)
        
        return jsonify({
          'success' : True,
          'have_results' : have_results,
          'questions' : questions, #question data object is not JSON serializable 
          'total_questions' : total_questions,
          'current_category' : 1
        })

    # Post a new question
    else: 
        if (question and answer and difficulty and category):
            try:
                new_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                new_question.insert()
            except:
                abort(422)
        else:
            abort(422)

        return jsonify({'success':True})


  # @TODO: (see above)
  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 

  # TEST: Search by any phrase. The questions list will update to include 
  # only question that include that string within their question. 
  # Try using the word "title" to start. 

  # @app.route('/questions/search', methods=['POST'])
  # def search_questions():
  #   pass

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id): 
    query_results = Question.query.filter_by(category=category_id).all()
    questions = [{'question': q.question, 'answer': q.answer, 'category': q.category, 'difficulty': q.difficulty} for q in query_results]
    total_questions = len(questions)

    if total_questions == 0:
        abort(404)

    response = jsonify({
      'success': True,
      'questions': questions,
      'total_questions': total_questions,
      'current_category': category_id 
    })

    return response 


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def play_trivia():
    print(request.data)
    data = json.loads(request.data)
    print('processed data')
    print(data)

    try: 
        previous_questions = data['previous_questions']
    except KeyError:
        previous_questions = None
    try:
        active_category = data['quiz_category']
    except KeyError:
        active_category = None
        abort(422)

    # print(previous_questions)
    print('active category: ')
    print(active_category)

    if previous_questions:
        # print('previous_quesitons is real.')
        questions = Question.query.filter(Question.category==active_category['id']).filter(
                    ~Question.id.in_(previous_questions)).all()
    else:
        # print('previous_quesitons is NOT REAL.')
        questions = Question.query.filter(Question.category==active_category['id']).all()
    
    try: 
        ids = [q.id for q in questions]
        length = len(ids)
        random_num = random.randrange(0, length - 1, 1)
        q = questions[random_num]

        # print(q)

        response = jsonify({
          'success': True,
          'question': {'question': q.question, 'answer': q.answer, 'category': q.category, 'difficulty': q.difficulty}
        })

        return response
    except:
        abort(422)


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
    }), 400

  @app.errorhandler(403)
  def forbidden(error):
    return jsonify({
      "success": False,
      "error": 403,
      "message": "Forbidden resource"
    }), 403

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method not allowed on this resource"
    }), 405

  @app.errorhandler(422)
  def unprocessable_request(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable request"
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal server error"
    }), 500



  return app

    