from django.shortcuts import render, get_object_or_404, redirect
from articlesboard.settings import SITE_NAME
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
# from dal import autocomplete

from .models import AdvUser, Category, Article, Tag
from .forms import ARegisterUserForm, ChangeUserInfoForm, ArticleForm, ArticleFormSet
from .utilities import signer

def index(request):
    rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]
    last_articles = Article.objects.filter(is_active=True)
    context = {'last_articles': last_articles, 'rate_articles': rate_articles, 'site_name': SITE_NAME}
    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]
    context = {'article': article, 'tags': article.tags.all(), 'site_name': SITE_NAME, 'rate_articles': rate_articles}
    return render(request, 'articles/article.html', context)


@login_required
def profile(request):
    rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]
    context = {'user': request.user, 'site_name': SITE_NAME, 'rate_articles': rate_articles}
    return render(request, 'articles/user_actions/profile.html', context)


# @login_required
class ChangeRatingView(UpdateView):
    
    success_url = reverse_lazy('articles:article')
    
    def get(self, request, rating, pk):
        # rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]
        article = Article.objects.get(pk=pk)
        article.rating_count += 1
        # context = {'user': request.user, 'site_name': SITE_NAME, 'rate_articles': rate_articles}
        if article.rating_count > 0:
            article.rating = (article.rating + rating)/article.rating_count
        else:
            article.rating = rating
        # messages.add_message(request, messages.SUCCESS, 'Рейтинг успешно изменен.')
        article.save()
        return super(ChangeRatingView, self)
    
    def get_queryset(self, request, rating, pk):
        # rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]
        article = Article.objects.get(pk=pk)
        article.rating_count += 1
        # context = {'user': request.user, 'site_name': SITE_NAME, 'rate_articles': rate_articles}
        if article.rating_count > 0:
            article.rating = (article.rating + rating)/article.rating_count
        else:
            article.rating = rating
        # messages.add_message(request, messages.SUCCESS, 'Рейтинг успешно изменен.')
        article.save()
        return super(ChangeRatingView, self)
    
    class Meta:
        model = Article


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


# @login_required
class ArticleAddView(TemplateView):

    # template_name = 'articles/add_article.html'

    def get(self, request):
        form = ArticleForm(initial={'author': request.user.pk})
        context = {'form': form, 'site_name': SITE_NAME}
        return render(request, 'articles/add_article.html', context=context)
    
    def post(self, request):
        form = ArticleForm(request.POST, request.FILES, initial={'author': request.user.pk})
        if form.is_valid():
            # urlx = form.cleaned_data['']
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Объявление отправлено на модерацию.')
        return redirect('articles:profile')

    class Meta:
        model = Article


class ALoginView(LoginView):
    extra_context = {'site_name': SITE_NAME}
    template_name = 'articles/user_actions/login.html'
    
    
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
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
