from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Article, Comments


# Create your views here.
# This view is to sort User articles alone
class MyArticlesView(LoginRequiredMixin, ListView):  
    template_name = 'my_view.html'

    def get_queryset(self):
        querryset = Article.objects.filter(author=self.request.user).order_by('-id')
        return querryset


class ArticleListView(LoginRequiredMixin, ListView):

    template_name = 'article_list.html'

    def test_func(self): # adds the user authomatically
        obj = self.get_object()
        return obj.author == self.request.user

    def get_queryset(self):
        queryset = Article.objects.all()
        queryset = queryset.order_by('-id')  # this line enables descending order
        return queryset


class ArticleDetailview(LoginRequiredMixin,  DetailView):
    model = Article
    template_name = 'article_detail.html'


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # new
    model = Article
    fields = ('title', 'body',)
    template_name = 'article_edit.html'

    def test_func(self): # new
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # new
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self): # Automatically adds the author field
        obj = self.get_object()  # this querry get the user 
        return obj.author == self.request.user  # returns the author


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentView(LoginRequiredMixin, CreateView):
    model = Comments
    template_name = 'add_comment.html'
    fields = ('comment',)


    def form_valid(self, form):  # makes variables to be added automatically
        form.instance.author = self.request.user
        form.instance.article = Article.objects.get(pk=self.kwargs['article_id'])
        return super().form_valid(form)


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comments
    template_name = 'comment_edit.html'
    fields = ('comment',)


    def form_valid(self, form):  # enables user and article ID to be added automatically
        form.instance.author = self.request.user
        form.instance.article = Article.objects.get(pk=self.kwargs['article_id'])
        return super().form_valid(form)


    def test_func(self): # adds the user authomatically
        obj = self.get_object()
        return obj.author == self.request.user


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comments
    template_name = 'comment_del.html'
    success_url = reverse_lazy('article_list')


    def test_func(self):  # this func enables django to add the user by default
        obj = self.get_object()
        return obj.author == self.request.user


class CommentDetailview(LoginRequiredMixin,  DetailView):
    model = Comments
    template_name = 'comment_detail.html'

