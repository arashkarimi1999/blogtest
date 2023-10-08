from django.urls import path

from . import views
app_name = "article"
urlpatterns = [
    path("articles-list", views.ArticlesView.as_view(), name="article-list"),
    path("articles-list/articles-comment", views.add_article_comment, name="add_article_comment"),
    path("articles-list/cat/<str:category>", views.ArticlesView.as_view(), name="article-by-category-list"),
    path("articles-list/<slug:slug>", views.ArticleDetailView.as_view(), name="article-detail"),
    path("create-article",views.CreateArticle.as_view(),name="Create-Article")
]
