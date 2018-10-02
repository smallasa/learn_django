from django.contrib import admin
from . import models
# Register your models here.


# 对于博客，需要定制一下显示方式
class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'visiting', 'created_time', 'modified_time']

# 注册
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Entry)