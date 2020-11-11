import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category
import random

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @Done: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @Done: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @Done: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    allcategories=Category.query.all()
    categories={}
    for category in allcategories:
      categories.update({
        category.id:category.type
        })

    return jsonify({
    "success":True,
    "categories":categories
    })
  
  '''
  @Done: 
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
  def get_questions():
    page=request.args.get('page', 1, type=int)
    start=(page-1)*QUESTIONS_PER_PAGE
    end=start+QUESTIONS_PER_PAGE
    questions=[]
    current_category=[]
    all_questions=Question.query.all()
    for question in all_questions:
      questions.append(Question.format(question))

    allcategories=Category.query.all()
    categories={}
    for category in allcategories:
      categories.update({
        category.id:category.type
        })

    total_questions= len(questions)
    questions_for_this_page=questions[start:end]
    for question in questions_for_this_page:
      current_category.append(question['category'])
    
    return jsonify({
      "success":True,
      "questions":questions[start:end],
      "total_questions":total_questions,
      "categories":categories,
      "current_category":current_category
      })

  '''
  @Done: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question=Question.query.filter_by(id=question_id).first()
    try:
      Question.delete(question)
      return jsonify({
        "success":True,
        "delete_question":"yes"
        })
    except:
      abort(422)

  '''
  @Done: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def add_question():
    body=request.get_json()
    question=body.get('question')
    answer=body.get('answer')
    category=body.get('category')
    difficulty=body.get('difficulty')
    try:
      new_question=Question(question=question, answer=answer, category=category, difficulty=difficulty)
      Question.insert(new_question)
      return jsonify({
        "success":True,
        "new question":"addedd"
        })
    except:
      abort(422)

  '''
  @Done: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    current_category=[]
    formated_questions=[]
    try:
      body=request.get_json()
      search_term=body.get('searchTerm')
      questions=Question.query.filter(Question.question.contains(search_term)).all()
      for question in questions:
        formated_questions.append(Question.format(question))
        current_category.append(question.category)
      return jsonify({
        "success":True,
        "questions":formated_questions,
        "total_questions":len(questions),
        "current_category":current_category
        })
    except:abort(400)
  '''
  @Done: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_for_this_category(category_id):
    formated_questions=[]
    current_category=[]
    allcategories=Category.query.all()
    categories=[]
    for category in allcategories:
      categories.append(
        category.id)
    if category_id in categories:
      questions=Question.query.filter_by(category=category_id).all()
      for question in questions:
        formated_questions.append(Question.format(question))
        current_category.append(question.category)
      return jsonify({
        "success":True,
        "questions":formated_questions,
        "total_questions":len(formated_questions),
        "current_category":current_category
        })
    else:
      abort(404)
  '''
  @Done: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    questions=[]
    formated_questions=[]
    try:
      body=request.get_json()
      category_object=body.get('quiz_category')
      category=category_object['id']
      if category==0:
        questions=Question.query.all()
      else:
        questions=Question.query.filter_by(category=category).all()
      for question in questions:
        formated_questions.append(Question.format(question))
      max=len(questions)
      random_num=random.randint(0,max)
      return jsonify({
        "success":True,
        "question":formated_questions[random_num]
        })
    except:
      abort(400)

  '''
  @Done: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success":False,
      "error":400,
      "message":"bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Resource Not found"
      }), 404

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
      "success":False,
      "error":405,
      "message":"Method not allowed"
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  
  return app
