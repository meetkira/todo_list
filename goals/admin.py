from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")

class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "description","status", "priority", "due_date", "category", "user", "created", "updated")
    search_fields = ("title", "user", "category")

class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("goal", "text", "user", "created", "updated")
    search_fields = ("title", "user", "category")

admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
