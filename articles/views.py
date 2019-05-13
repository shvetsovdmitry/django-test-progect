from django.shortcuts import render
from articlesboard.settings import SITE_NAME
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView

from .models import AdvUser, Category, Article
from .forms import ARegisterUserForm


def index(request):
    rate_articles = Article.objects.order_by('-rating')[:10]
    last_articles = Article.objects.filter(is_active=True)
    context = {'last_articles': last_articles, 'rate_articles': rate_articles, 'site_name': SITE_NAME}
    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    rate_articles = Article.objects.order_by('-rating')[:10]
    context = {'article': article, 'tags': article.tags.all(), 'site_name': SITE_NAME, 'rate_articles': rate_articles}
    return render(request, 'articles/article.html', context)


@login_required
def profile(request):
    rate_articles = Article.objects.order_by('-rating')[:10]
    context = {'user': request.user, 'site_name': SITE_NAME, 'rate_articles': rate_articles}
    return render(request, 'articles/user_actions/profile.html', context)


class ALoginView(LoginView):
    extra_context = {'site_name': SITE_NAME}
    success_url = reverse_lazy('articles:index')
    template_name = 'articles/user_actions/login.html'
    
    
class ALogoutView(LoginRequiredMixin, LogoutView):
    extra_context = {'site_name': SITE_NAME}
    template_name = 'articles/user_actions/logout.html'
    
    
class ARegisterUserView(CreateView):
    model = AdvUser
    template_name = 'articles/user_actions/register_user.html'
    form_class = ARegisterUserForm
    success_url = reverse_lazy('articles:register_done')