from django.db import models
from datetime import date
from django.db.models import Count
from django.contrib.auth.models import User


########### Managers ###########

class TagManager(models.Manager):
    def hot(self):
        return Tag.objects.annotate(number_of_questions=Count('question')).order_by('-number_of_questions')[:7]
        
class QuestionManager(models.Manager):
    def new(self):
        return self.all().order_by('-date').annotate(number_of_answers=Count('answer'))

    def hot(self):
        return self.all().order_by('-rating').annotate(number_of_answers=Count('answer'))

    def tag(self, tag):
        return self.filter(tags__name__exact=tag).annotate(number_of_answers=Count('answer')).order_by('-date')

    def current_question(self, id):
        return self.filter(id=id).first()

class AnswerManager(models.Manager):
    def by_question(self, q_id):
        return self.filter(question_id=q_id).order_by('-rating')

########### Models ###########

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, default = "../static/img/no-user.jpg", upload_to='upload/')
    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length = 60)
    def __str__(self):
        return self.name
    objects = TagManager()

class Question(models.Model):
    title = models.TextField(max_length = 200)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField()
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    def calc_rating(self, mark):
        self.rating = self.rating + mark
        self.save()
    objects = QuestionManager()

class QuestionMark(models.Model):
    author = models.ForeignKey(Profile, on_delete = models.CASCADE)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    LIKE = 1
    DISLIKE = -1
    like_choice = [(LIKE, "like"), (DISLIKE, "dislike")]
    mark = models.SmallIntegerField(choices=like_choice)
 
class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)    
    text = models.TextField()
    date = models.DateField()
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default = False)
    objects = AnswerManager()
    def __str__(self):
        return self.question.title
    def calc_rating(self, mark):
        self.rating = self.rating + mark
        self.save()

class AnswerMark(models.Model):
    author = models.ForeignKey(Profile, on_delete = models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete = models.CASCADE)
    LIKE = 1
    DISLIKE = -1
    like_choice = [(LIKE, "like"), (DISLIKE, "dislike")]
    mark = models.SmallIntegerField(choices=like_choice)




