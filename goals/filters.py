import django_filters
from django.db import models

from goals.models import Goal, GoalComment


class GoalDateFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Goal
        fields = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }

class CommentGoalFilter(django_filters.rest_framework.FilterSet):
    goal = django_filters.ModelChoiceFilter(field_name="goal__title", queryset=Goal.objects.all())

    class Meta:
        model = GoalComment
        fields = ("goal",)