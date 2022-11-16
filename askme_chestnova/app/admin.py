from django.contrib import admin
from app.models import Question
from app.models import Profile
from app.models import Answer
from app.models import Tag
from app.models import AnswerMark
from app.models import QuestionMark



admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(AnswerMark)
admin.site.register(QuestionMark)

