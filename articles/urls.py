from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('<int:pk>/<slug:slug>', views.ArticleDetailView.as_view(), name='article-details'),
    path('list', views.ArticlesListView.as_view(), name='articles-list'),

]
