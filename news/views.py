from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news/posts.html'  # Добавили news/ в начало
    context_object_name = 'posts'
