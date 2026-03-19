from django.urls import path, include

from .views import PostsList, PostDetail, SearchPosts
from .views import ArticleCreate, ArticleUpdate, ArticleDelete
from .views import NewsCreate, NewsUpdate, NewsDelete
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchPosts.as_view(), name='search_posts'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', PostsList.as_view(), name='home'),
]
