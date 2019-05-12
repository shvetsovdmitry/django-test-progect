from django.shortcuts import render
from .models import AdvUser, Rubric, Article


def index(request):
    articles = Article.objects.filter(is_active=True)[:10]
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)