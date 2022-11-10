from django.shortcuts import render
from django.core.paginator import Paginator
from . import models

def paginate(obj_list, request):
    paginator = Paginator(obj_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def index(request):
    objects = paginate(models.QUESTIONS, request)
    context = {'is_auth': True, 'page_obj': objects }
    return render(request, 'index.html', context=context)


def hot(request):
    objects = paginate(models.QUESTIONS, request)
    context = {'is_auth': True, 'page_obj': objects}
    return render(request, 'hotquestions.html', context=context) 

def question(request, question_id: int ):
    objects = paginate(models.ANSWERS, request)
    question_item = models.QUESTIONS[question_id]
    context = {'question': question_item,
    'page_obj': objects,
    'is_auth': False }
    return render(request, 'question.html', context=context)

def ask(request):
    context = {'is_auth': True}
    return render(request, 'ask.html', context=context)

def tag(request, tag: str):
    objects = paginate(models.QUESTIONS, request)
    context = {'page_obj': objects, 'tag': tag, 'is_auth': True}
    return render(request, 'tag.html', context=context)

def settings(request):
    context = {'user': models.USERS[0], 'is_auth': True}
    return render(request, 'settings.html', context=context)

def login(request):
    context = {'is_auth': False}
    return render(request, 'login.html', context=context)

def signup(request):
    context = {'is_auth': False}
    return render(request, 'signup.html', context=context)
