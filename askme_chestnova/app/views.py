from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage
from . import models
from .models import Question, Answer, Tag
from django.http import HttpResponse, HttpResponseNotFound
from django.http import Http404

def paginate(obj_list, request):
    paginator = Paginator(obj_list, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except InvalidPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj

def index(request):    
    questions = Question.objects.new()
    objects = paginate(questions, request)
    tags = Tag.objects.hot()
    context = {'is_auth': True, 'page_obj': objects, 'tags': tags }
    return render(request, 'index.html', context=context)


def hot(request):
    questions = Question.objects.hot()
    objects = paginate(questions, request)
    tags = Tag.objects.hot()
    context = {'is_auth': True, 'page_obj': objects, 'tags': tags}
    return render(request, 'hotquestions.html', context=context) 

def question(request, question_id: int):
    question_item = Question.objects.current_question(question_id)
    answers = Answer.objects.by_question(question_id)
    objects = paginate(answers, request)    
    tags = Tag.objects.hot()    
    context = {'item': question_item,
    'page_obj': objects,
    'is_auth': True,
    'tags': tags }
    return render(request, 'question.html', context=context)

def ask(request):
    tags = Tag.objects.hot()
    context = {'is_auth': True, 'tags': tags}
    return render(request, 'ask.html', context=context)

def tag(request, tag_name):
    questions = Question.objects.tag(tag_name)
    objects = paginate(questions, request)
    tags = Tag.objects.hot()
    context = {'page_obj': objects, 'tag': tag_name, 'is_auth': True, 'tags': tags}
    return render(request, 'tag.html', context=context)

def settings(request):
    tags = Tag.objects.hot()    
    context = {'user': models.USERS[0], 'is_auth': True, 'tags': tags}
    return render(request, 'settings.html', context=context)

def login(request):
    tags = Tag.objects.hot() 
    context = {'is_auth': False, 'tags': tags}
    return render(request, 'login.html', context=context)

def signup(request):
    tags = Tag.objects.hot() 
    context = {'is_auth': False, 'tags': tags}
    return render(request, 'signup.html', context=context)
