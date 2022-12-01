from django.urls import path
from .views import (ArticleListView,
                    ArticleDetailview,
                    ArticleCreateView,
                    ArticleDeleteView,
                    ArticleUpdateView,
                    CommentView,
                    CommentUpdate,
                    CommentDelete,
                    MyArticlesView,)


urlpatterns = [
        path('', ArticleListView.as_view(), name='article_list'),
        path('<int:pk>/', ArticleDetailview.as_view(), name='article_detail'),
        path('new/', ArticleCreateView.as_view(), name='article_new'),
        path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
        path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
        path('comment/<int:article_id>/', CommentView.as_view(), name='add_comment'),
        path('<int:article_id>/<int:comments_id>/comment_edit/', CommentUpdate.as_view(), name='comment_edit'),
        path('<int:article_id>/<int:comments_id>/comment_del/', CommentDelete.as_view(), name='comment_del'),
        path('my_view/', MyArticlesView.as_view(), name='my_view'),
]
