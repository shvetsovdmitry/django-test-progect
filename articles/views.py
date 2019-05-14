from django.shortcuts import render, get_object_or_404
from articlesboard.settings import SITE_NAME
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from .models import AdvUser, Category, Article
from .forms import ARegisterUserForm
from .utilities import signer

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


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'articles/user_actions/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'articles/user_actions/user_is_activated.html'
    else:
        template = 'articles/user_actions/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class ALoginView(LoginView):
    extra_context = {'site_name': SITE_NAME}
    template_name = 'articles/user_actions/login.html'
    success_url = reverse_lazy('articles:index') 
    
    
class ALogoutView(LoginRequiredMixin, LogoutView):
    extra_context = {'site_name': SITE_NAME}
    template_name = 'articles/user_actions/logout.html'
    
    
class ARegisterUserView(CreateView):
    model = AdvUser
    template_name = 'articles/user_actions/register_user.html'
    form_class = ARegisterUserForm
    success_url = reverse_lazy('articles:register_done')
    
    
class ARegisterDoneView(TemplateView):
    template_name = 'articles/user_actions/register_done.html'
