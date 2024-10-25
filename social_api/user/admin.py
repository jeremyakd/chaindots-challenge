from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)


admin.site.register(User, UserAdmin)
