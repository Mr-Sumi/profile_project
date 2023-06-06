from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ClintProfile, Category, KeySkill, UserProfile, Notification


class UserProfileInline(admin.StackedInline):
    model = ClintProfile
    can_delete = False
    verbose_name_plural = 'User Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(ClintProfile)

admin.site.register(Category)
admin.site.register(KeySkill)
admin.site.register(UserProfile)
admin.site.register(Notification)