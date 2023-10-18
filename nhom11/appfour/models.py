from django import forms
import django
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models import deletion
from django.db.models.base import Model
import os

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    #additional
    portfolio_size = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic',blank=True)

    def __str__(self):
        return self.user.username



class Post(models.Model):
    #authour = models.OneToOneField(User,on_delete=models.CASCADE)
    id = models.AutoField(primary_key = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=265)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image_post = models.ImageField(upload_to='image_post/',blank=True,null = True)
    # status = models.BooleanField(default=True)

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    # comments = models.ManyToManyField(Comment, blank=True)

    def __str__(self):
        return self.title

class Draft(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=265)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image_post = models.ImageField(upload_to='image_post/',blank=True,null = True)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.title
        
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    id = models.AutoField(primary_key = True)
    #name = models.CharField(max_length=255)
    body = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.user)



class DraftComment(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=265)
    #post = models.ForeignKey(Post, related_name="comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    body = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

