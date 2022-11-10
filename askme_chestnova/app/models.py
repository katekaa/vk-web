from django.db import models

USERS = [
    {
        'id': user_id,
        'name': f'User{user_id}',
        'photo': f"img/user{user_id}.jpg",
        'login': f'login user{user_id}',
        'email': f'user{user_id}@gmail.com',
        'password': '123456'
    }
    for user_id in range(3)
]

QUESTIONS = [
    {
        'id': question_id,
        'title': f'Question {question_id}',
        'text': f'Text of question #{question_id}',
        'answers_number': question_id+question_id+2,
        'tags': ['tag1' for i in range(question_id)],
        'rating': question_id+2,
        'user': USERS[question_id % 3]
    }
   for question_id in range(21)
   
]

ANSWERS = [
    {
        'id': answer_id,
        'title': f'Answer {answer_id}',
        'text': f'Text of answer #{answer_id}',
        'rating': answer_id+2,
        'user': USERS[answer_id % 2 ]
    }
   for answer_id in range(10)
   
]


