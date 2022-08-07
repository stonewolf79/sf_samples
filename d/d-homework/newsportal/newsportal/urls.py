from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

from main.views import *

def get_ignore(request):
    return HttpResponse('')

urlpatterns = [
    path('', NewsList.as_view(), name='start'),
    path('admin/', admin.site.urls),
    path('news/', NewsList.as_view(), name='news'),
    path('news/<int:pk>/', PostInfo.as_view(), name='news_info'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_del'),
    path('articles/', PostList.as_view(), name='articles'),
    path('articles/<int:pk>/', PostInfo.as_view()),
    path('articles/create/', PostCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', PostEdit.as_view()),
    path('articles/<int:pk>/delete/', PostDelete.as_view()),
    path('favicon.ico', get_ignore),

    path('sign/', include('sign.urls')),
    path('profile/', Profile.as_view(), name='profile'),
    path('accounts/', include('allauth.urls')),
]
