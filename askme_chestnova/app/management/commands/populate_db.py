from django.core.management.base import BaseCommand
from ...models import *
from django.core.files import File
from faker import Faker
import faker.providers
import random
from itertools import islice
from collections import OrderedDict


IMAGES = [
    "user0.jpg",
    "user1.jpg",
    "user2.jpg",
    "user3.jpg",
    "user4.jpg",
    "user5.jpg",
    "user6.jpg",
    "user7.jpg",
]

symbols = [".", ",", "-", "_", ":", " ", "!", "&", "?"]


class Provider(faker.providers.BaseProvider):
    def profile_avatar(self):
        return self.random_element(IMAGES)


fake = Faker(locale="ru_RU")
fake.add_provider(Provider)
Faker.seed(0)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("-t", "--tags", type=int)
        parser.add_argument("-u", "--users", type=int)
        parser.add_argument("-q", "--questions", type=int)
        parser.add_argument("-qm", "--question_marks", type=int)
        parser.add_argument("-a", "--answers", type=int)
        parser.add_argument("-am", "--answer_marks", type=int)
        parser.add_argument("-all", "--all", type=int)

    def handle(self, *args, **options):
        num_t = options["tags"]
        num_u = options["users"]
        num_q = options["questions"]
        num_qm = options["question_marks"]
        num_a = options["answers"]
        num_am = options["answer_marks"]
        num_all = options["all"]

        if num_all:
            self.fill_with_tags(num_all)
            self.fill_with_users(num_all)
            self.fill_with_questions(num_all * 10)
            self.fill_with_question_marks(num_all * 100)
            self.fill_with_answers(num_all * 100)
            self.fill_with_answer_marks(num_all * 100)
        if num_t:
            self.fill_with_tags(num_t)
        if num_u:
            self.fill_with_users(num_u)
        if num_q:
            self.fill_with_questions(num_q)
        if num_qm:
            self.fill_with_question_marks(num_qm)
        if num_a:
            self.fill_with_answers(num_a)
        if num_am:
            self.fill_with_answer_marks(num_am)

    def fill_with_tags(self, num):
        fake.random.seed(random.randint(1, num))
        batch_size = min(num, 10000)

        objs = (Tag(name=(fake.word()+random.choice(symbols)+fake.word()))
                for _ in range(num))
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            Tag.objects.bulk_create(batch, batch_size)

    def fill_with_users(self, num):
        for i in range(num):
            u = User.objects.create(username=(fake.user_name() + str(random.randint(-9, 9)) + fake.name()+random.choice(symbols) + str(random.randint(-9, 9)) + random.choice(symbols) + random.choice(symbols) +
                                              fake.first_name() + random.choice(symbols) + str(random.randint(-9, 9))), password=fake.password(), email=fake.email())
            Profile.objects.create(user=u)

        profiles = Profile.objects.all()
        for p in profiles:
            pic = fake.profile_avatar()
            img = File(open("./static/img/" + pic, "rb"))
            p.avatar = img
            p.save(update_fields=["avatar"])

    def fill_with_questions(self, num):
        authors = list(Profile.objects.values_list("id", flat=True))
        tags = list(Tag.objects.values_list("id", flat=True))
        for i in range(min(num, 10000)):
            q = Question.objects.create(title=fake.unique.sentence()[:60][:-1] + '?',
                                        author_id=random.choice(authors),
                                        text=fake.unique.paragraph(
                nb_sentences=10),
                date=fake.unique.date_time_between(
                "-100d", "now"),
                rating=0)
            for _ in range(1, random.randint(2, 5)):
                q.tags.add(random.choice(tags))

    def fill_with_answers(self, num):
        authors = list(Profile.objects.values_list("id", flat=True))
        questions = list(Question.objects.values_list("id", flat=True))
        for i in range(min(num, 10000)):
            a = Answer.objects.create(author_id=random.choice(authors),
                                      question_id=random.choice(questions),
                                      text=fake.unique.paragraph(
                nb_sentences=8),
                date=fake.unique.date_time_between(
                "-100d", "now"),
                rating=0)

    def fill_with_answer_marks(self, num):
        authors = list(Profile.objects.values_list("id", flat=True))
        answers = list(Answer.objects.values_list("id", flat=True))
        objs = []
        for i in range(num):
            a = AnswerMark(author_id=random.choice(authors),
                           answer_id=random.choice(answers),
                           mark=random.choice([-1, 1]))
            a.answer.calc_rating(a.mark)
            objs.append(a)
        batch_size = min(num, 10000)
        while True:
            batch = list(islice(objs, batch_size))
            del objs[:batch_size]
            if not batch:
                break
            AnswerMark.objects.bulk_create(batch, batch_size)

    def fill_with_question_marks(self, num):
        authors = list(Profile.objects.values_list("id", flat=True))
        questions = list(Question.objects.values_list("id", flat=True))
        objs = []
        for i in range(num):
            q = QuestionMark(author_id=random.choice(authors),
                             question_id=random.choice(questions),
                             mark=random.choice([-1, 1]))
            q.question.calc_rating(q.mark)
            objs.append(q)
        batch_size = min(num, 10000)
        while True:
            batch = list(islice(objs, batch_size))
            del objs[:batch_size]
            if not batch:
                break
            QuestionMark.objects.bulk_create(batch, batch_size)
