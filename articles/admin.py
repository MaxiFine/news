from django.contrib import admin
from .models import Article, Comments


class CommentInline(admin.TabularInline): # new
    model = Comments
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
    CommentInline,
    ]

# Register your models here.
admin.site.register(Article)
admin.site.register(Comments)

