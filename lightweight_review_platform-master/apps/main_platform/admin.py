from django.contrib import admin
from .models import Question, Tag, Hotspot, CommonWeaknessCategory, CommonWeaknessTag
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):

    fields = ['title', 'tags', 'category', 'answer', 'note', 'user_belong']

    list_display = ['title', 'category', 'user_belong', 'created_time']


class HotSpotAdmin(admin.ModelAdmin):

    fields = ['title', 'content']

    list_display = ['title', 'date']


class CommonWeaknessCategoryAdmin(admin.ModelAdmin):

    fields = ['name']

    list_display = ['name']


class CommonWeaknessTagAdmin(admin.ModelAdmin):

    fields = ['name', 'category_belong']

    list_display = ['name']



admin.site.register(Question, QuestionAdmin)
admin.site.register(Hotspot, HotSpotAdmin)
admin.site.register(CommonWeaknessCategory, CommonWeaknessCategoryAdmin)
admin.site.register(CommonWeaknessTag, CommonWeaknessTagAdmin)

