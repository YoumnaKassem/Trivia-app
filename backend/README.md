# Full Stack Trivia API Backend

### Installing Dependencies

#### Python 3.7

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask]

- [SQLAlchemy]
- [Flask-CORS]

## Running the server

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Endpoints :
GET '/categories'
GET '/questions'
DELETE /questions/<int:question_id>'
POST '/questions'
POST '/questions/search'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

-----------------------------------------

GET '/questions'
-Fetches a list of 10 questions based on page argument, incase that no argument, the default page is 1
-Request Arguments: 'page' to choose page number, the default value is 1
-Returns: A list of question objects, success value, No. of total questions, dictionary of categories in which the keys are the ids and the value is the corresponding string of the category, and a list of categories.
-Results are paginated in group of 10. 
{
"questions":[{
  'id': 1,
  'question': 'Is Egypt located in Africa?',
  'answer': 'yes',
  'category': 3,
  'difficulty': 1
 },
 {
  'id': 2,
  'question': 'Is Germany located in Europe?',
  'answer': 'yes',
  'category': 3,
  'difficulty': 1
 }]
 "success":True,
 "total_questions":2,
 "current_category":[2]
}


--------------------------------------------

DELETE '/questions/<int:question_id>'

-Delete a particular question based on a given question id.
-Request argument: question_id
-Returns success value.
{
"success":True
}

-------------------------------------------

POST '/questions'

-Create a new question using a submitted question,answer, current category and level of difficultey.
-Request argument: None
-Returns success value.
{
  "success":True
}

-------------------------------------------

POST '/questions/search'

-search for questions that contain any part of search term.
-Request argument: None
-Return list of questions that contain search using a submitted search button, success value, number of questions, and current categories.
{
"success":True,
"questions":[{
  'id': 1,
  'question': 'Is there real acrylic colors?',
  'answer': 'may be',
  'category': 5,
  'difficulty': 1
 },
 {
  'id': 2,
  'question': 'how many muscles in our body',
  'answer': 'more than 300',
  'category': 3,
  'difficulty': 1
 }],
"total_questions":2,
"current_category":[3,5]
}

---------------------------------------
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
