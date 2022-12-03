from django.shortcuts import render, redirect
from django.core.paginator import Paginator, InvalidPage
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from app.forms import *
from .models import Question, Answer, Tag
from django.http import HttpResponseRedirect


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
    context = {'is_auth': True, 'page_obj': objects, 'tags': tags}
    return render(request, 'index.html', context=context)


def hot(request):
    questions = Question.objects.hot()
    objects = paginate(questions, request)
    tags = Tag.objects.hot()
    context = {'is_auth': True, 'page_obj': objects, 'tags': tags}
    return render(request, 'hotquestions.html', context=context)


def question(request, question_id: int):
    question_item = Question.objects.current_question(question_id)
    answers = Answer.objects.by_question(question_id).order_by('-rating')
    objects = paginate(answers, request)
    tags = Tag.objects.hot()
    a_form = AnswerForm()
    
    if request.method == "POST":
        a_form = AnswerForm(request.POST)
        if a_form.is_valid():
            answer = Answer.objects.create(author=request.user.profile,
            question=question_item,
            text = a_form.cleaned_data['text'])
            answer.save()
            answers = Answer.objects.by_question(question_id).order_by('-rating')
            objects=paginate(answers, request)
            return HttpResponseRedirect('/question/%s/?page=%s'  % (question_id, objects.paginator.num_pages))
    context = {'item': question_item,
               'page_obj': objects,
               'tags': tags,
               'form': a_form}
    return render(request, 'question.html', context=context)

@login_required
def ask(request):
    tags = Tag.objects.hot()
    if request.method == 'GET':
        q_form = AskForm()
    if request.method == "POST":
        q_form = AskForm(request.POST)
        if q_form.is_valid():
            q_tags = q_form.save()
            question = Question.objects.create(author=request.user.profile,
                                               title=q_form.cleaned_data["title"],
                                               text=q_form.cleaned_data["text"])
            for tag in q_tags:
                question.tags.add(tag)
            question.save()
            return redirect('question', question_id = question.pk)
    return render(request, 'ask.html', {'tags': tags, 'q_form': q_form})


def tag(request, tag_name):
    questions = Question.objects.tag(tag_name)
    objects = paginate(questions, request)
    tags = Tag.objects.hot()
    context = {'page_obj': objects, 'tag': tag_name,
               'is_auth': True, 'tags': tags}
    return render(request, 'tag.html', context=context)


@login_required
def settings(request):
    tags = Tag.objects.hot()
    if request.method == 'GET':
        user_form = UserSettingsForm(initial={'username': request.user.username, 'email': request.user.email})
        profile_form = ProfileSettingsForm(initial={'avatar': request.user.profile.avatar})
    if request.method == "POST":
        user_form = UserSettingsForm(request.POST, instance=request.user)
        profile_form = ProfileSettingsForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
    return render(request, 'settings.html', {'tags': tags, 'user_form': user_form, 'profile_form': profile_form})


def login(request):
    tags = Tag.objects.hot()
    valuenext=""
    if request.method == "GET": 
        user_form = LoginForm() 
        valuenext = request.GET.get('next')        

    if request.user.is_authenticated:
        return redirect('index')        
    
    if request.method == "POST":
        valuenext= request.POST.get('next')
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                if valuenext == "":
                    return redirect('index')
                else:                    
                    return redirect(valuenext)

    return render(request, 'login.html', {'tags': tags, 'form': user_form, 'valuenext': valuenext})


def signup(request):
    tags = Tag.objects.hot()
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        user_form = SignUpForm()

    if request.method == 'POST':
        user_form = SignUpForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()

            if user:
                auth.login(request, user)
                return redirect('index')

    return render(request, 'signup.html', {'form': user_form, 'tags': tags})

@login_required
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def password_change(request):
    tags = Tag.objects.hot()
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST, )
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('settings')
    else: 
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password_change.html', {'form': form, 'tags': tags})
