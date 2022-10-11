from rest_framework import permissions

from goals.models import BoardParticipant, GoalCategory, Goal


class BoardPermissions(permissions.IsAuthenticated):
    """
    Permissions для досок.
    Получить информацию может любой участник доски.
    Редактировать/удалять информацию может только владелец доски.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermissions(permissions.IsAuthenticated):
    """
    Permissions для категорий.
    Получить информацию может любой участник доски, к которой относится категория.
    Редактировать/удалять информацию может только владелец/редактор доски.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "DELETE":
            category = GoalCategory.objects.get(id=request.parser_context["kwargs"]["pk"])
            board_id = category.board.id
        else:
            board_id = request.data.get("board")
        return BoardParticipant.objects.filter(
            user=request.user, board_id=board_id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()

    def has_object_permission(self, request, view, obj):
        _filter = {
            'user': request.user,
            'board': obj.board,
        }

        if request.method not in permissions.SAFE_METHODS:
            _filter.update({
                'role__in': [
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer
                ]
            })

        return BoardParticipant.objects.filter(**_filter).exists()


class GoalPermissions(permissions.IsAuthenticated):
    """
    Permissions для целей.
    Получить информацию может любой участник доски, к которой относится цель.
    Редактировать/удалять информацию может только владелец/редактор доски.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "DELETE":
            goal = Goal.objects.get(id=request.parser_context["kwargs"]["pk"])
            id_ = goal.category_id
        else:
            id_ = request.data.get("category")
        goal_category = GoalCategory.objects.get(id=id_)
        return BoardParticipant.objects.filter(
            user=request.user, board=goal_category.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()

    def has_object_permission(self, request, view, obj):
        _filter = {
            'user': request.user,
            'board': obj.category.board,
        }
        if request.method not in permissions.SAFE_METHODS:
            _filter.update({
                'role__in': [
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer
                ]
            })
        return BoardParticipant.objects.filter(**_filter).exists()


class GoalCommentPermissions(permissions.IsAuthenticated):
    """
    Permissions для комментариев.
    Получить информацию может любой участник доски, к которой относится комментарий.
    Редактировать/удалять информацию может только пользователь, написавший комментарий.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.data.get("goal"):
            if isinstance(request.data.get("goal"), int):
                goal = Goal.objects.get(id=request.data.get("goal"))
                goal_category = GoalCategory.objects.get(id=goal.category_id)
            else:
                goal_category = GoalCategory.objects.get(id=request.data.get("goal")["category"])
            return BoardParticipant.objects.filter(
                user=request.user, board=goal_category.board,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
            ).exists()
        return True
