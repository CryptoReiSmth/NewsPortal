from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .models import Post
from .forms import PostForm


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


# Поиск
class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news/search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'N'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'A'
        return super().form_valid(form)
