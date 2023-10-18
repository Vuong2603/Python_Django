from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import fields
from appfour.models import  Post,Comment,UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_size','profile_pic')

class PostForm(forms.ModelForm):
    class Meta():
        modelpost = Post
        fieldpost = ('title','body','date','image_post')

class CommentForm(forms.ModelForm):
    class Meta():
        modelcomment = Comment
        fieldscomment = ('post','user','body','date_comment')

class Post_Update(forms.ModelForm):
    class Meta():
        modelpost = Post
        fieldpost = ('title','body','date','image_post')
        
class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100)

