from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryAdmin(admin.ModelAdmin):
    """Админка для модели категория"""
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user__username")


class GoalAdmin(admin.ModelAdmin):
    """Админка для модели цель"""
    list_display = ("title", "description", "status", "priority", "due_date", "category", "user", "created", "updated")
    search_fields = ("title", "user__username", "category__title")
    list_filter = ("status", "priority", "due_date")


class GoalCommentAdmin(admin.ModelAdmin):
    """Админка для модели комментарий"""
    list_display = ("goal", "text", "user", "created", "updated")
    search_fields = ("text", "user__username")


class BoardAdmin(admin.ModelAdmin):
    """Админка для модели доска"""
    list_display = ("title", "created", "updated")
    search_fields = ("title", )


class BoardParticipantAdmin(admin.ModelAdmin):
    """Админка для модели участник доски"""
    list_display = ("board", "user", "role")
    search_fields = ("board__title", "user__username")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
