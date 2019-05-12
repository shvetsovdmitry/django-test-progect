from django.shortcuts import render
from .models import AdvUser, Rubric, Article


def index(request):
    articles = Article.objects.filter(is_active=True)[:10]
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {'article': article}
    return render(request, 'articles/article.html', context)