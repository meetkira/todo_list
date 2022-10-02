from rest_framework import permissions

from goals.models import BoardParticipant, GoalCategory, Goal


class BoardPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermissions(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return BoardParticipant.objects.filter(
            user=request.user, board_id=request.data.get("board"),
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

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        goal_category = GoalCategory.objects.get(id=request.data.get("category"))
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
