from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "github_username"]

    list_filter = ["is_staff", "is_active", "date_joined"]    

    search_fields = ["username", "email", "github_username"]

admin.site.register(User, CustomUserAdmin)
