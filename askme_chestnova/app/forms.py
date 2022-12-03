from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from datetime import date
from django.core.files import File


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(min_length=3, widget=forms.PasswordInput)

    def clean(self):
        if not User.objects.filter(username=self.cleaned_data['username']).exists():
            raise ValidationError("Wrong username or password")
        else:
            user = User.objects.get(username=self.cleaned_data['username'])
            password = user.password
            if not check_password(self.cleaned_data['password'], password):
                raise ValidationError("Wrong username or password")
        return self.cleaned_data


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        min_length=3, max_length=90, widget=forms.TextInput)
    password = forms.CharField(
        min_length=4, max_length=50, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length=4, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        data = self.cleaned_data
        password_1 = data['password']
        password_2 = data['password_check']

        if User.objects.filter(username=data['username']).exists():
            raise ValidationError("Username already taken")

        if password_1 != password_2:
            raise ValidationError("Passwords don't match")

        return data

    def save(self):
        data = self.cleaned_data

        user = User.objects.create_user(
            username=data['username'], password=data['password'], email=data['email'])
        if data['avatar'] is None:
            p = Profile.objects.create(user=user)
            img = File(open("./static/img/no-user.jpg", "rb"))
            p.avatar = img
            p.save(update_fields=["avatar"])
        else:
            Profile.objects.create(user=user, avatar=data['avatar'])
        return user


class UserSettingsForm(forms.ModelForm):
    username = forms.CharField(min_length=3, max_length=90)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileSettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=True)

    class Meta:
        model = Profile
        fields = ['avatar']


class AskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput)
    text = forms.CharField(widget=forms.Textarea, required=True)
    tags = forms.CharField(required=False, max_length=90,
                           help_text="Enter tags separated by space")

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def save(self):
        data = self.cleaned_data
        all_tags = data['tags'].split()
        q_tags = []
        for tag in all_tags:
            t = Tag.objects.filter(name=tag).first()
            if t is None:
                t = Tag.objects.create(name=tag)
            q_tags.append(t)
        return q_tags


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Type your answer here',
                                                        'class': 'form-control',
                                                        'id': 'inputAnswer',
                                                        'style': 'margin-bottom: 10px;'}), required=True)

    class Meta:
        model = Answer
        fields = ['text']
