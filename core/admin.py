from django.contrib import admin

# Register your models here.
from core.models import User


@admin.register(User)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("email", "first_name", "last_name", "username")
    list_filter = ("is_staff", "is_active", "is_superuser")
    exclude = ("password",)
    readonly_fields = ("last_login", "date_joined")
