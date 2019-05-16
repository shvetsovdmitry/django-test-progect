from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
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


@login_required
def change_rating(request, rating, pk):       
        article = Article.objects.get(pk=pk)
        article.change_rating(rating)
        messages.add_message(request, messages.SUCCESS, 'Спасибо! Ваш голос учтен.')
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


def previous_page(request, previous_page):
    return HttpResponseRedirect(previous_page)


# @login_required
class ArticleAddView(TemplateView):

    # template_name = 'articles/add_article.html'

    def get(self, request):
        form = ArticleForm(initial={'author': request.user.pk})
        rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]
        context = {'form': form, 'site_name': SITE_NAME, 'rate_articles': rate_articles}
        return render(request, 'articles/add_article.html', context=context)
    
    # def previous_page(self):
    #     return redirect(self.request.META.get('HTTP_REFERER'))
    
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


# class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
#     model = AdvUser
#     template_name = 'articles/user_actions/change_user_info.html'
#     # form_class = ChangeUserInfoForm
#     # success_url = reverse_lazy('articles:profile')
#     # success_message = 'Личные данные пользователя изменены'

#     def post(self, request):
#         user = get_object_or_404(AdvUser, pk=request.user.pk)
#         form = ChangeUserInfoForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             user = form.save()
#             messages.add_message(request, messages.SUCCESS, 'Профиль изменен.')
#             return redirect('articles:profile')
#         else:
#             messages.add_message(request, messages.WARNING, 'Профиль не был изменен.')
#             return reverse_lazy('articles:profile_change')
            
#     def get(self, request):
#         user = get_object_or_404(AdvUser, pk=request.user.pk)
#         form = ChangeUserInfoForm(instance=user)
#         context = {'form': form}
#         return render(request, 'articles/user_actions/change_user_info.html', context)
    

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



@login_required
def change_user_info(request):
    user = get_object_or_404(AdvUser, pk=request.user.pk)
    if request.method == 'POST':
        form = ChangeUserInfoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            # formset = AIFormSet(request.POST, request.FILES, instance=bb)
            # if formset.is_valid():
            #     formset.save()
            messages.add_message(request, messages.SUCCESS, 'Профиль изменен')
            return redirect('articles:profile')
    else:
        form = ChangeUserInfoForm(instance=user)
        # formset = AIFormSet(instance=bb)
    context = {'form': form}
    return render(request, 'articles/user_actions/change_user_info.html', context)



# def change_user_info(request, pk):
#     article = get_object_or_404(Article, pk=pk)
#     if request.method