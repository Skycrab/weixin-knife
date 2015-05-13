#coding=utf8

from django.contrib import admin
from models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')

    # def save_model(self, request, obj, form, change):
    #     pass

admin.site.register(Category, CategoryAdmin)