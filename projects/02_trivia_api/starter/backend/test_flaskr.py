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
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_404_delete_non_existent_question(self):
        res = self.client().delete('/questions/1001')

        self.assertEqual(res.status_code, 404)

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()