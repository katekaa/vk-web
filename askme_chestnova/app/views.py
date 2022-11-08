PYTHONPATH="D:\vk_ed\vk-web\askme_chestnova\venv\lib\site-packages"


from django.shortcuts import render
from . import models

def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context=context)

def question(request, question_id: int ):
    return render(request, 'question.html')

