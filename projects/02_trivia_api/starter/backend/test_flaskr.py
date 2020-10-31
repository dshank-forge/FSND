import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least two tests for each endpoint- one for the successful operation and one for the expected error(s).
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['categories'], ['Science', 'Art', 'Geography', 
                                              'History', 'Entertainment', 'Sports'])

    def test_405_for_post_categories(self):
        res = self.client().post('/categories')

        self.assertEqual(res.status_code, 405)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['categories'], ['Science', 'Art', 'Geography', 
                                              'History', 'Entertainment', 'Sports'])
        self.assertTrue(data['current_category'])

    def test_405_delete_questions(self):
        res = self.client().delete('/questions')

        self.assertEqual(res.status_code, 405)

    def test_delete_question_by_id(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_422_delete_non_existent_question(self):
        res = self.client().delete('/questions/1001')

        self.assertEqual(res.status_code, 422)

    def test_create_question(self):
        question = 'what is the capital of Vermont?'
        answer = 'Montpelier'
        difficulty = 4
        category = 2
        question_record = {'question': question, 'answer': answer, 'difficulty': difficulty, 'category': category}
        
        res = self.client().post('/questions', json=question_record)
        data = json.loads(res.data)

        try:
            Q = Question.query.filter_by(question=question).one()
        except:
            Q = Question(question='q', answer='a', difficulty=1, category=2)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(Q.answer, answer)

    def test_422_bad_question_post(self):
        question = None
        answer = 'a'
        difficulty = '1'
        category = 'geography'

        res = self.client().post('/questions?answer=' + answer + '&difficulty=' + str(difficulty) + '&category=' + category)
        # data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
     
    def test_search_yes_results(self):
        phrase = 'who'
        # res = self.client().post('/questions?searchTerm=' + phrase)
        res = self.client().post('/questions', json={'searchTerm': phrase})
        data = json.loads(res.data)
        print('returned data:' + str(data))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['have_results'], True)
    
    def test_search_no_results(self):
        phrase = 'zzZyYyyyxX'
        res = self.client().post('/questions', json={'searchTerm': phrase})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['have_results'], False)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions']) 

    def test_404_get_questions_bad_category(self):
        res = self.client().get('/categories/1001/questions')

        self.assertEqual(res.status_code, 404)

    def test_return_next_quiz_question(self):
        res = self.client().post('/quizzes', json={'previous_questions':[5,6,9],'quiz_category':2})
        data = json.loads(res.data)

        # print(data)
        returned_question = data['question']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(returned_question)
        self.assertEqual(returned_question['category'], 2)

    def test_422_no_active_category(self):  
        res = self.client().post('/quizzes', json={'previous_questions':[5,6,9]})

        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()