from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from articlesboard.settings import SITE_NAME
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.utils import timezone
# from django.contrib.sites.models import Site

from .models import AdvUser, Category, Article, Tag
# , ArticleStatistics
from .forms import ARegisterUserForm, ChangeUserInfoForm, ArticleForm, ArticleFormSet
from .utilities import signer


rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]
# current_site = Site.objects.get_current()


def index(request):
    last_articles = Article.objects.filter(is_active=True)
    context = {'last_articles': last_articles, 'rate_articles': rate_articles, 'site_name': SITE_NAME}
    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user not in article.viewed_users.all():
        if request.user.is_authenticated:
            article.viewed_users.add(request.user)
        article.views += 1
        article.save()
    context = {'article': article, 'tags': article.tags.all(), 'site_name': SITE_NAME, 'rate_articles': rate_articles}
    return render(request, 'articles/article.html', context)


@login_required
def profile(request, username):
    user = get_object_or_404(AdvUser, username=username)
    context = {'user': user, 'rate_articles': rate_articles, 'site_name': SITE_NAME}
    return render(request, 'articles/user_actions/profile.html', context)


@login_required
def change_rating(request, rating, pk):
    article = Article.objects.get(pk=pk)
    if request.user not in article.rated_users.all():
        article.change_rating(rating)
        article.rated_users.add(request.user)
        messages.add_message(request, messages.SUCCESS, 'Спасибо! Ваш голос учтен.')
    else:
        messages.add_message(request, messages.WARNING, 'Вы уже голосовали за эту статью!')
    global rate_articles
    rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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


class ArticleAddView(TemplateView, LoginRequiredMixin):

    template_name = 'articles/add_article.html'

    def get(self, request):
        form = ArticleForm(initial={'author': request.user.pk})
        context = {'form': form, 'site_name': SITE_NAME, 'rate_articles': rate_articles}
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        form = ArticleForm(request.POST, request.FILES, initial={'author': request.user.pk})
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Объявление отправлено на модерацию.')
        return redirect('articles:profile')

    class Meta:
        model = Article


class ALoginView(LoginView):

    extra_context = {'site_name': SITE_NAME}
    template_name = 'articles/user_actions/login.html'
    
    redirect_field_name = reverse_lazy('articles:index')
    redirect_authenticated_user = True
    
    def get(self, *args):
        return render(self.request, self.template_name, self.extra_context)

    def post(self, *args):
        user = authenticate(self.request, username=self.request.POST['username'], password=self.request.POST['password'])
        if user is not None:
            login(self.request, user)
            return redirect(self.redirect_field_name)
        else:
            messages.add_message(self.request, messages.ERROR, 'Неправильный логин или пароль')
    
    
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
 

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'articles/user_actions/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('articles:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
    
    def get(self, request):
        self.user = get_object_or_404(AdvUser, pk=self.user_id)
        form = ChangeUserInfoForm(instance=self.user)
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = ChangeUserInfoForm(request.POST, request.FILES, instance=self.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Профиль изменен')
            return redirect('articles:profile')
