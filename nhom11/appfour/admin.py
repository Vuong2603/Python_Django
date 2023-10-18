from django import forms
from django.contrib import admin
from appfour.models import  UserProfileInfo,Post,Draft,DraftComment,Comment
#from .models import Fields

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Draft)
admin.site.register(DraftComment)

# admin.site.register(ModelFieldsAdmin)
