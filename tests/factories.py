import datetime

import factory.django

from core.models import User
from goals.models import GoalCategory, Board, BoardParticipant, Goal, GoalComment


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker("name")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "testuser"
    password = factory.PostGenerationMethodCall('set_password', 'testuserpassword')


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Faker("name")
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Faker("name")
    description = factory.Faker("sentence")
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)
    due_date = datetime.date.today()


class GoalCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text = factory.Faker("sentence")
    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)
