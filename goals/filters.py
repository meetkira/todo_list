import django_filters
from django.db import models

from goals.models import Goal, GoalComment
from rest_framework.filters import OrderingFilter


class GoalCommentOrdering(OrderingFilter):
    """Фильтр для комментариев к цели"""
    allowed_custom_filters = ['created', 'updated']

    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering[0] == 'created':
                return [f"-{ordering[0]}"]
            else:
                return ordering

        return self.get_default_ordering(view)


class GoalOrdering(OrderingFilter):
    """Фильтр для порядка расположения целей"""
    allowed_custom_filters = ['title', 'created', 'due_date', 'priority']

    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering[0] != 'due_date':
                return [f"-{ordering[0]}"]
            else:
                return ordering

        return self.get_default_ordering(view)


class GoalDateFilter(django_filters.rest_framework.FilterSet):
    """Фильтр для выбора целей по полям"""
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
