import json

from django.db import transaction
from django.forms import model_to_dict
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from goals.filters import GoalDateFilter, CommentGoalFilter, GoalCommentOrdering, GoalOrdering
from goals.models import GoalCategory, Goal, GoalComment, Board, Status
from goals.permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, GoalCommentPermissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardSerializer, \
    BoardListSerializer


# GoalCategory -----------------
class GoalCategoryCreateView(CreateAPIView):
    """Создание категории"""
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """Получение списка категорий с поддержкой фильтрации и пангинации"""
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        query = Board.objects.filter(participants__user=self.request.user)
        if self.request.query_params.get("board"):
            query = Board.objects.filter(id=self.request.query_params.get("board"))
        return GoalCategory.objects.filter(board__in=query, is_deleted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if request.query_params.get("limit") or request.query_params.get("offset"):
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """Получение/обновление/удаление категории"""
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        Goal.objects.filter(category=instance).update(
            status=Status.archived, is_deleted=True
        )
        instance.save()
        return instance


# Goal -----------------
class GoalCreateView(CreateAPIView):
    """Создание цели"""
    model = GoalCategory
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    """Получение списка целей с поддержкой фильтрации и пангинации"""
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        GoalOrdering,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering = ["title"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(is_deleted=False)


class GoalView(RetrieveUpdateDestroyAPIView):
    """Получение/обновление/удаление цели"""
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.status = Status.archived
        instance.save()
        return instance


# GoalComment -----------------
class GoalCommentCreateView(CreateAPIView):
    """Создание комментария"""
    model = GoalComment
    permission_classes = [GoalCommentPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    """Получение списка комментариев с поддержкой фильтрации и пангинации"""
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        GoalCommentOrdering,
        DjangoFilterBackend,
    ]
    filterset_class = CommentGoalFilter
    ordering = ["created"]

    def get_queryset(self):
        return GoalComment.objects.filter(goal_id=self.request.query_params["goal"])


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    """Получение/обновление/удаление комментария"""
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [GoalCommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.all()


# Board -----------------
class BoardCreateView(CreateAPIView):
    """Создание доски"""
    model = Board
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    """Получение списка досок с поддержкой фильтрации и пангинации"""
    model = Board
    permission_classes = [IsAuthenticated]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ["title"]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if request.query_params.get("limit") or request.query_params.get("offset"):
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BoardView(RetrieveUpdateDestroyAPIView):
    """Получение/обновление/удаление доски"""
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Status.archived, is_deleted=True
            )
        return instance
