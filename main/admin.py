from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('Phone',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('Phone',)}),
    )
    list_display = ['username', 'Phone', 'is_staff']
    search_fields = ['Phone', 'username']


admin.site.register(User, CustomUserAdmin)