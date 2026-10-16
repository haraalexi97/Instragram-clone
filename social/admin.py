from django.contrib import admin
from .models import Profile, Follow, Post, Like, Comment
admin.site.register([Profile, Follow, Post, Like, Comment])
