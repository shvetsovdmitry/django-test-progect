from django.urls import path

from .views import index, detail

app_name = 'articles'
urlpatterns = [
    path('articles/<int:pk>', detail, name='article'),
    path('', index, name='index'),
]
