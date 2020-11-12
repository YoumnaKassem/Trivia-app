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
        self.database_name = "trivia"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','0000','localhost:5432', 'trivia')
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test""" 
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res=self.client().get('/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
        
    def test_delete_question(self):
        res=self.client().delete('/questions/10')
        data=json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete_question'])

    def test_post_question(self):
        res=self.client().post('/questions', json={'question': 'Is Egypt located in Africa?',
            'answer': 'yes',
            'category': 2,
            'difficulty': 3})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_questions_with_results(self):
        res=self.client().post('/questions/search', json={'searchTerm':'the'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_search_questions_without_results(self):
        res=self.client().post('/questions/search', json={'searchTerm':'sdgdsgs'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)


    def test_get_questions_in_that_category(self):
        res=self.client().get('/categories/4/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_play_quiz(self):
        res=self.client().post('/quizzes', json={'quiz_category': {'id': 0 }})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_400_bad_request(self):
        res=self.client().post('/questions/search')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_404_not_found(self):
        res=self.client().get('/categories/265/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_405_method_not_allowed(self):
        res=self.client().post('/questions/50', json={'question': 'Is England located in Asia?',
            'answer': 'No',
            'category': 2,
            'difficulty': 4})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)

    def test_422_unprocessable(self):
        res=self.client().delete('/questions/345')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()