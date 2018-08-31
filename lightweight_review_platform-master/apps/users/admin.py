from django.contrib import admin
from .models import UserProfile, UserWeaknessCategory, UserWeaknessTag
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):

    fields = ['username', 'password', 'email', 'nickname', 'gender', 'birthday', 'presentCollege', 'targetCollege', 'avatar', 'motto', 'checkin_days', 'lastCheckinDate', 'memo']

    list_display = ['username', 'email', 'nickname']


class UserWeaknessCategoryAdmin(admin.ModelAdmin):

    fields = ['name', 'user_belong']

    list_display = ['name']


class UserWeaknessTagAdmin(admin.ModelAdmin):

    fields = ['name', 'category_belong']

    list_display = ['name']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserWeaknessCategory, UserWeaknessCategoryAdmin)
admin.site.register(UserWeaknessTag, UserWeaknessTagAdmin)
