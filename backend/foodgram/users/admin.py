
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User, Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    list_display_links = ('username',)
    list_filter = ('email', 'username')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'email')}),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user', 'author')
