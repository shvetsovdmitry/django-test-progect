from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

from .models import AdvUser, Category, Article


def index(request):
    rate_articles = Article.objects.order_by('-rating')[:10]
    last_articles = Article.objects.filter(is_active=True)
    context = {'last_articles': last_articles, 'rate_articles': rate_articles}
    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {'article': article, 'tags': article.tags.all()}
    return render(request, 'articles/article.html', context)


class ALoginView(LoginView):
    template_name = 'main/login.html'
    
    
class ALogoutView(LogoutView):
    template_name = 'main/logout.html'