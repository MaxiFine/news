from django.shortcuts import render

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Article, Comments


# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    login_url = 'login'
    template_name = 'article_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['Article'] = Article.objects.all()
    #     context['user_specific'] = Article.objects.filter(get_user_model, self.request.user)
    #     return context

    # def get_queryset(self):
    #     return Article.objects.all() # Get 5 books containing the title war

    # def get_context_data(self):
    #     context = super().get_context_data()
    #     context["user_specific"] = Article.objects.get(id=self.kwargs["list_id"])
    #     return context



class ArticleDetailview(LoginRequiredMixin,  DetailView):
    model = Article
    template_name = 'article_detail.html'
    login_url = 'login'


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # new
    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'
    login_url = 'login'

    def test_func(self): # new
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # new
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def test_func(self): # Automatically adds the author field
        obj = self.get_object()  # this querry get the user 
        return obj.author == self.request.user  # returns the author


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body',)
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentView(LoginRequiredMixin, CreateView):
    model = Comments
    template_name = 'add_comment.html'
    fields = ('comment',)
    login_url = 'login'


    def form_valid(self, form):  # makes variables to be added automatically
        form.instance.author = self.request.user
        form.instance.article = Article.objects.get(pk=self.kwargs['article_id'])
        return super().form_valid(form)


class CommentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comments
    template_name = 'comment_edit.html'
    fields = ('comment',)
    login_url = 'login'


    def form_valid(self, form):  # makes variables to be added automatically
        form.instance.author = self.request.user
        form.instance.article = Article.objects.get(pk=self.kwargs['article_id'])
        return super().form_valid(form)


    def test_func(self): # new
        obj = self.get_object()
        return obj.author == self.request.user


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comments
    template_name = 'comment_del.html'
    fields = ('comment',)
    login_url = 'login'

    def test_func(self): # new
        obj = self.get_object()
        return obj.author == self.request.user
