from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from articlesboard.settings import SITE_NAME
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.forms import ValidationError

# from dal import autocomplete
from tagging.models import TaggedItem, Tag

from tagging_autocomplete.models import TagAutocomplete

from .models import AdvUser, Category, Article
from .forms import ARegisterUserForm, ChangeUserInfoForm, ArticleForm, ArticleFormSet
from .forms import DeleteArticleForm, EditArticleForm
from .utilities import signer


# Popular articles.
rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]


# Main page view.
def index(request):
    last_articles = Article.objects.filter(is_active=True)
    # Refreshing popular articles.
    rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]
    context = {'last_articles': last_articles, 'rate_articles': rate_articles, 'site_name': SITE_NAME}
    return render(request, 'articles/index.html', context)


# Article page view.
def detail(request, pk):
    article = Article.objects.get(pk=pk)
    # Check if current user already read the article.
    if request.user not in article.viewed_users.all():
        if request.user.is_authenticated:
            article.viewed_users.add(request.user)
        article.views += 1
        article.save()
    # Get TaggedItem objects related to article.
    tags_objs = TaggedItem.objects.filter(object_id=pk)
    tags = []
    for tag in tags_objs:
        tags.append(tag.tag)
    context = {'article': article, 'tags': tags, 'site_name': SITE_NAME, 'rate_articles': rate_articles}
    return render(request, 'articles/article.html', context)


# Profile page view.
def profile(request, username=None):
    # Get AdvUser object by username.
    if username is None:
        username = request.user.username
    user = get_object_or_404(AdvUser, username=username)
    context = {'user': user, 'rate_articles': rate_articles, 'site_name': SITE_NAME}
    return render(request, 'articles/user_actions/profile.html', context)


# When user press rating button.
@login_required
def change_rating(request, rating, pk):
    article = Article.objects.get(pk=pk)
    if request.user not in article.rated_users.all():
        article.change_rating(rating, request.user)
        messages.add_message(request, messages.SUCCESS, 'Спасибо! Ваш голос учтен.')
    else:
        messages.add_message(request, messages.WARNING, 'Вы уже голосовали за эту статью!')
    # Refresh current rate_articles.
    global rate_articles
    rate_articles = Article.objects.order_by('-rating').filter(is_active=True)[:10]
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Post-registration activation controller.
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'articles/user_actions/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'articles/user_actions/user_already_activated.html'
    else:
        template = 'articles/user_actions/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


@login_required
def subscribe_user(request, username):
    user = AdvUser.objects.get(username=username)
    if user not in request.user.user_subscriptions.all():
        request.user.subscribe_user(user)
    else:
        messages.add_message(request, messages.WARNING, 'Вы уже подписаны на этого пользователя!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_user(request, username):
    user = AdvUser.objects.get(username=username)
    if user in request.user.user_subscriptions.all():
        request.user.unsubscribe_user(user)
    else:
        messages.add_message(request, messages.WARNING, 'Вы не подписаны на этого пользователя!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def subscribe_tag(request, tag):
    tag = Tag.objects.get(name=tag)
    if tag not in request.user.tags_subscriptions.all():
        request.user.subscribe_tag(tag)
    else:
        messages.add_message(request, messages.WARNING, 'Вы уже подписаны на этот тег')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_tag(request, tag):
    tag = Tag.objects.get(name=tag)
    if tag in request.user.tags_subscriptions.all():
        request.user.unsubscribe_tag(tag)
    else:
        messages.add_message(request, messages.WARNING, 'Вы не подписаны на этот тег')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def search_by_tag(request, tag):
    articles = Article.objects.filter(tags__contains=tag)
    tag = Tag.objects.get(name=tag)
    if tag not in request.user.tags_subscriptions.all():
        url = reverse_lazy('articles:subscribe_tag', kwargs={'tag': tag})
        subscribe_btn = f'''<a href="{url}" class="btn btn-outline-secondary btn-block">
        <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
        width="32" height="32" viewBox="0 0 192 192" style=" fill:#000000;">
        <g fill="none" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" 
        stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" 
        font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal">
        <path d="M0,192v-192h192v192z" fill="none" stroke="none"></path>
        <g stroke="none"><g id="surface1">
        <path d="M180,75.26953c-0.35156,-1.05469 -1.28906,-1.80469 -2.40234,-1.92187l-60,
        -5.46094l-22.07812,-54c-0.44531,-1.04297 -1.46484,-1.71094 -2.58984,-1.71094c-1.13672,
        0 -2.15625,0.66797 -2.60156,1.71094l-22.07812,54l-60,5.46094c-1.11328,0.11719 -2.0625,
        0.87891 -2.40234,1.94531c-0.35156,1.06641 -0.02344,2.23828 0.80859,2.97656l45.26953,
        39.59766l-13.91016,57c-0.23437,1.10156 0.21094,2.22656 1.11328,2.87109c0.91406,0.65625 2.12109,
        0.70313 3.08203,0.12891l50.55469,-31.46485l50.69531,31.38281c0.96094,0.5625 2.16797,0.51563 3.08203,
        -0.14062c0.90235,-0.64453 1.34766,-1.76953 1.11328,-2.85937l-13.92187,-57l45.28125,-39.60937c0.86719,
        -0.67969 1.25391,-1.82812 0.98438,-2.90625z" fill="#f9e3ae"></path>
        <path d="M180,75.26953c-0.35156,-1.05469 -1.28906,-1.80469 -2.40234,-1.92187l-60,-5.46094l-22.07812,
        -54c-0.375,-1.08984 -1.37109,-1.83984 -2.51953,-1.88672v134.51953l50.46094,31.26563c0.96094,0.5625 2.16797,
        0.51563 3.08203,-0.14062c0.90235,-0.64453 1.34766,-1.76953 1.11328,-2.85937l-13.92187,-57l45.28125,
        -39.60937c0.86719,-0.67969 1.25391,-1.82812 0.98438,-2.90625z" fill="#f6d397"></path>
        <path d="M186,74.07422c-0.36328,-1.14844 -1.38281,-1.96875 -2.57812,-2.07422l-64.26562,-5.82422l-23.60156,
        -57.86719c-0.46875,-1.125 -1.5586,-1.86328 -2.77735,-1.86328c-1.21875,0 -2.32031,0.73828 -2.77734,
        1.86328l-23.61328,57.86719l-64.10156,5.82422c-1.20703,0.10547 -2.22656,0.91406 -2.60156,2.0625c-0.36328,
        1.13672 -0.02344,2.40234 0.89063,3.1875l48.38672,42.30469l-15,60.77344c-0.29297,1.18359 0.15234,2.4375 1.14844,
        3.15234c0.98438,0.71485 2.30859,0.76172 3.35156,0.11719l54.30469,-33.59766l54.23438,33.63281c1.03125,0.64453 2.36719,
        0.59765 3.35156,-0.11719c0.98438,-0.72656 1.4414,-1.96875 1.14844,-3.15234l-15,-60.78516l48.38672,
        -42.29297c0.9961,-0.73828 1.44141,-2.01562 1.11328,-3.21094zM131.25,116.25c-0.85547,0.75 -1.20703,
        1.91016 -0.92578,3l13.67578,55.40625l-49.65234,-30.65625c-0.96094,-0.59766 -2.17969,-0.59766 -3.15234,
        0l-49.52344,30.65625l13.55859,-55.44141c0.28125,-1.08984 -0.08203,-2.25 -0.92578,-3l-44.4961,-39l58.95703,
        -5.21484c1.10156,-0.10547 2.0625,-0.82031 2.48438,-1.86328l21.51563,-52.73437l21.53906,52.73438c0.41015,
        1.04297 1.37109,1.75781 2.48438,1.86328l58.94531,5.36719z" fill="#8d6c9f"></path>
        <path d="M9,117c-1.65234,0 -3,1.34766 -3,3v6c0,1.65234 1.34766,3 3,3c1.65234,0 3,-1.34766 3,-3v-6c0,
        -1.65234 -1.34766,-3 -3,-3z" fill="#8d6c9f"></path>
        <path d="M24,117c-1.65234,0 -3,1.34766 -3,3v6c0,1.65234 1.34766,3 3,3c1.65234,0 3,-1.34766 3,-3v-6c0,
        -1.65234 -1.34766,-3 -3,-3z" fill="#8d6c9f"></path>
        <path d="M42,126v-6c0,-1.65234 -1.34766,-3 -3,-3c-1.65234,0 -3,1.34766 -3,3v6c0,1.65234 1.34766,3 3,
        3c1.65234,0 3,-1.34766 3,-3z" fill="#8d6c9f"></path>
        <path d="M144,120v6c0,1.65234 1.34766,3 3,3c1.65234,0 3,-1.34766 3,-3v-6c0,-1.65234 -1.34766,-3 -3,
        -3c-1.65234,0 -3,1.34766 -3,3z" fill="#8d6c9f"></path>
        <path d="M162,117c-1.65234,0 -3,1.34766 -3,3v6c0,1.65234 1.34766,3 3,3c1.65234,0 3,
        -1.34766 3,-3v-6c0,-1.65234 -1.34766,-3 -3,-3z" fill="#8d6c9f"></path>
        <path d="M177,117c-1.65234,0 -3,1.34766 -3,3v6c0,1.65234 1.34766,3 3,3c1.65234,0 3,
        -1.34766 3,-3v-6c0,-1.65234 -1.34766,-3 -3,-3z" fill="#8d6c9f"></path>
        <path d="M96,72c0,-1.65234 -1.34766,-3 -3,-3c-1.65234,0 -3,1.34766 -3,3v24h-24c-1.65234,
        0 -3,1.34766 -3,3c0,1.65234 1.34766,3 3,3h24v24c0,1.65234 1.34766,3 3,3c1.65234,0 3,-1.34766 3,
        -3v-24h24c1.65234,0 3,-1.34766 3,-3c0,-1.65234 -1.34766,-3 -3,-3h-24z" fill="#8d6c9f"></path></g></g>
        <g stroke="none"><g id="Layer_1">
        <circle cx="31" cy="35" transform="scale(3,3)" r="12" fill="#72caaf"></circle>
        <path d="M111,102h-15v-15c0,-1.656 -1.344,-3 -3,-3c-1.656,0 -3,1.344 -3,3v15h-15c-1.656,0 -3,
        1.344 -3,3c0,1.656 1.344,3 3,3h15v15c0,1.656 1.344,3 3,3c1.656,0 3,-1.344 3,-3v-15h15c1.656,0 3,
        -1.344 3,-3c0,-1.656 -1.344,-3 -3,-3z" fill="#f9efde"></path>
        <path d="M93,144c-21.504,0 -39,-17.496 -39,-39c0,-21.504 17.496,-39 39,-39c21.504,0 39,17.496 39,
        39c0,21.504 -17.496,39 -39,39zM93,72c-18.195,0 -33,14.805 -33,33c0,18.195 14.805,33 33,33c18.195,
        0 33,-14.805 33,-33c0,-18.195 -14.805,-33 -33,-33z" fill="#8d6c9f"></path></g></g>
        <path d="M54,144v-78h78v78z" id="overlay-drag" fill="#ff0000" stroke="none" opacity="0"></path></g></svg>
         Подписаться</a>'''
    else:
        url = reverse_lazy('articles:unsubscribe_tag', kwargs={'tag': tag})    
        subscribe_btn = f'''<a href="{url}" class="btn btn-outline-secondary btn-block">
        <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="32" height="32" viewBox="0 0 192 192" style=" fill:#000000;">
        <g fill="none" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" 
        stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" 
        font-size="none" text-anchor="none" style="mix-blend-mode: normal">
        <path d="M0,192v-192h192v192z" fill="none" stroke="none"></path>
        <g stroke="none"><g id="surface1">
        <path d="M180,75.26953c-0.35156,-1.05469 -1.28906,-1.80469 -2.40234,
        -1.92187l-60,-5.46094l-22.07812,-54c-0.44531,-1.04297 -1.46484,
        -1.71094 -2.58984,-1.71094c-1.13672,0 -2.15625,0.66797 -2.60156,
        1.71094l-22.07812,54l-60,5.46094c-1.11328,0.11719 -2.0625,0.87891
         -2.40234,1.94531c-0.35156,1.06641 -0.02344,2.23828 0.80859,2.97656l45.26953,
         39.59766l-13.91016,57c-0.23437,1.10156 0.21094,2.22656 1.11328,2.87109c0.91406,
         0.65625 2.12109,0.70313 3.08203,0.12891l50.55469,-31.46485l50.69531,31.38281c0.96094,
         0.5625 2.16797,0.51563 3.08203,-0.14062c0.90235,-0.64453 1.34766,-1.76953 1.11328,
         -2.85937l-13.92187,-57l45.28125,-39.60937c0.86719,-0.67969 1.25391,-1.82812 0.98438,
         -2.90625z" fill="#f9e3ae"></path>
        <path d="M180,75.26953c-0.35156,-1.05469 -1.28906,-1.80469 -2.40234,-1.92187l-60,
        -5.46094l-22.07812,-54c-0.375,-1.08984 -1.37109,-1.83984 -2.51953,-1.88672v134.51953l50.46094,
        31.26563c0.96094,0.5625 2.16797,0.51563 3.08203,-0.14062c0.90235,-0.64453 1.34766,
        -1.76953 1.11328,-2.85937l-13.92187,-57l45.28125,-39.60937c0.86719,-0.67969 1.25391,
        -1.82812 0.98438,-2.90625z" fill="#f6d397"></path>
        <path d="M186,74.07422c-0.36328,-1.14844 -1.38281,-1.96875 -2.57812,-2.07422l-64.26562,
        -5.82422l-23.60156,-57.86719c-0.46875,-1.125 -1.5586,-1.86328 -2.77735,-1.86328c-1.21875,
        0 -2.32031,0.73828 -2.77734,1.86328l-23.61328,57.86719l-64.10156,5.82422c-1.20703,
        0.10547 -2.22656,0.91406 -2.60156,2.0625c-0.36328,1.13672 -0.02344,2.40234 0.89063,
        3.1875l48.38672,42.30469l-15,60.77344c-0.29297,1.18359 0.15234,2.4375 1.14844,3.15234c0.98438,
        0.71485 2.30859,0.76172 3.35156,0.11719l54.30469,-33.59766l54.23438,33.63281c1.03125,
        0.64453 2.36719,0.59765 3.35156,-0.11719c0.98438,-0.72656 1.4414,-1.96875 1.14844,-3.15234l-15,
        -60.78516l48.38672,-42.29297c0.9961,-0.73828 1.44141,-2.01562 1.11328,-3.21094zM131.25,116.25c-0.85547,
        0.75 -1.20703,1.91016 -0.92578,3l13.67578,55.40625l-49.65234,-30.65625c-0.96094,-0.59766 -2.17969,
        -0.59766 -3.15234,0l-49.52344,30.65625l13.55859,-55.44141c0.28125,-1.08984 -0.08203,-2.25 -0.92578,
        -3l-44.4961,-39l58.95703,-5.21484c1.10156,-0.10547 2.0625,-0.82031 2.48438,-1.86328l21.51563,
        -52.73437l21.53906,52.73438c0.41015,1.04297 1.37109,1.75781 2.48438,1.86328l58.94531,
        5.36719z" fill="#8d6c9f"></path>
        <path d="M9,117c-1.65234,0 -3,1.34766 -3,3v6c0,1.65234 1.34766,3 3,3c1.65234,0 3,-1.34766 3,
        -3v-6c0,-1.65234 -1.34766,-3 -3,-3z" fill="#8d6c9f"></path><path d="M24,117c-1.65234,0 -3,1.34766 -3,
        3v6c0,1.65234 1.34766,3 3,3c1.65234,0 3,-1.34766 3,-3v-6c0,-1.65234 -1.34766,-3 -3,-3z" fill="#8d6c9f"></path>
        <path d="M42,126v-6c0,-1.65234 -1.34766,-3 -3,-3c-1.65234,0 -3,1.34766 -3,3v6c0,
        1.65234 1.34766,3 3,3c1.65234,0 3,-1.34766 3,-3z" fill="#8d6c9f"></path><path d="M144,
        120v6c0,1.65234 1.34766,3 3,3c1.65234,0 3,-1.34766 3,-3v-6c0,-1.65234 -1.34766,-3 -3,
        -3c-1.65234,0 -3,1.34766 -3,3z" fill="#8d6c9f"></path><path d="M162,117c-1.65234,0 -3,
        1.34766 -3,3v6c0,1.65234 1.34766,3 3,3c1.65234,0 3,-1.34766 3,-3v-6c0,-1.65234 -1.34766,
        -3 -3,-3z" fill="#8d6c9f"></path><path d="M177,117c-1.65234,0 -3,1.34766 -3,3v6c0,1.65234 1.34766,
        3 3,3c1.65234,0 3,-1.34766 3,-3v-6c0,-1.65234 -1.34766,-3 -3,-3z" fill="#8d6c9f"></path>
        <path d="M96,72c0,-1.65234 -1.34766,-3 -3,-3c-1.65234,0 -3,1.34766 -3,3v24h-24c-1.65234,0 -3,
        1.34766 -3,3c0,1.65234 1.34766,3 3,3h24v24c0,1.65234 1.34766,3 3,3c1.65234,0 3,-1.34766 3,
        -3v-24h24c1.65234,0 3,-1.34766 3,-3c0,-1.65234 -1.34766,-3 -3,-3h-24z" fill="#8d6c9f"></path>
        </g></g><g stroke="none"><g id="Layer_1"><circle cx="30.66667" cy="35.33333"
        transform="scale(3,3)" r="12" fill="#ed7899"></circle><path d="M96.059,106.186l10.812,
        -10.812c1.173,-1.173 1.173,-3.069 0,-4.242c-1.173,-1.173 -3.069,-1.173 -4.242,0l-10.812,
        10.812l-10.446,-10.446c-1.173,-1.173 -3.069,-1.173 -4.242,0c-1.173,1.173 -1.173,3.069 0,
        4.242l10.443,10.443l-10.443,10.443c-1.173,1.173 -1.173,3.069 0,4.242c0.585,0.585 1.353,
        0.879 2.121,0.879c0.768,0 1.536,-0.294 2.121,-0.879l10.443,-10.443l10.443,10.443c0.585,
        0.585 1.353,0.879 2.121,0.879c0.768,0 1.536,-0.294 2.121,-0.879c1.173,-1.173 1.173,
        -3.069 0,-4.242z" fill="#faefde"></path><path d="M92,145c-21.504,0 -39,-17.496 -39,-39c0,
        -21.504 17.496,-39 39,-39c21.504,0 39,17.496 39,39c0,21.504 -17.496,39 -39,39zM92,73c-18.195,
        0 -33,14.805 -33,33c0,18.195 14.805,33 33,33c18.195,0 33,-14.805 33,-33c0,-18.195 -14.805,
        -33 -33,-33z" fill="#8d6c9f"></path></g></g><path d="M53,145v-78h78v78z"
        id="overlay-drag" fill="#ff0000" stroke="none" opacity="0"></path>
        </g></svg> Отписаться</a>'''
    context = {'rate_articles': rate_articles, 'site_name': SITE_NAME, 'articles': articles, 'sub': subscribe_btn}
    return render(request, 'articles/search.html', context)


# Add article page view.
class ArticleAddView(TemplateView, LoginRequiredMixin):

    template_name = 'articles/user_actions/add_article.html'

    def get(self, request, *args, **kwargs):
        form = ArticleForm(initial={'author': self.request.user.pk})
        context = {'form': form, 'site_name': SITE_NAME, 'rate_articles': rate_articles}
        return render(self.request, self.template_name, context=context, *args)
    
    def post(self, request):
        form = ArticleForm(self.request.POST, self.request.FILES, initial={'author': self.request.user.pk})
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Статья отправлена на модерацию.')
        else:
            messages.add_message(self.request, messages.WARNING, 'Ошибка')
        return redirect('articles:index')

    class Meta:
        model = Article
        fields = ('__all__', )


class ArticleEditView(UpdateView, SuccessMessageMixin, LoginRequiredMixin):
    
    template_name = 'articles/user_actions/edit_article.html'
    model = Article
    form_class = EditArticleForm
    
    def dispatch(self, request, pk, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=pk)
        self.user_id = self.article.pk
        self.success_url = reverse_lazy('articles:article', kwargs={'pk': self.article.pk})
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.article.pk)
    
    def get(self, request):
        form = EditArticleForm(instance=self.article)
        context = {'article': self.article, 'form': form, 'site_name': SITE_NAME, 'rate_articles': rate_articles}
        return render(self.request, self.template_name, context=context)
    
    def post(self, request):
        form = EditArticleForm(self.request.POST, self.request.FILES, instance=self.article)
        if form.is_valid():
            self.article.is_active = False
            self.article.save()
            messages.add_message(self.request, messages.SUCCESS, 'Статья успешно отредактирована и отправлена на модерацию.')
        else:
            messages.add_message(self.request, messages.WARNING, 'Ошибка.')
            return redirect('articles:edit_article', pk=self.article.pk)
        return redirect('articles:index')
    
    class Meta:
        model = Article
        fields = ('__all__', )
        

# Confirm deletion of article page.
class ArticleDeleteView(TemplateView, LoginRequiredMixin):
    
    template_name = 'articles/user_actions/delete_article.html'
    
    def get(self, *args, pk):
        article = get_object_or_404(Article, pk=pk)
        form = DeleteArticleForm()
        context = {'form': form, 'article': article, 'site_name': SITE_NAME, 'rate_articles': rate_articles}
        return render(self.request, self.template_name, context)
    
    def post(self, *args, pk):
        form = DeleteArticleForm(self.request.POST)
        article = get_object_or_404(Article, pk=pk)
        if form.is_valid():
            # Restricting deletion from other users.
            if self.request.user.username.__ne__(article.author.username) and self.request.user.username.__ne__('admin'):
                messages.add_message(self.request, messages.ERROR, f'У пользователя {self.request.user.username} недостаточно прав для удаления данной статьи.')
                return redirect('articles:index')
            
            article.is_active = False
            article.save()
            messages.add_message(self.request, messages.SUCCESS, 'Статья успешно удалена')
        else:
            messages.add_message(self.request, messages.WARNING, 'Возникла ошибка во время удаления статьи!')
        return redirect('articles:index')
            

# Login page view.
class ALoginView(LoginView):

    extra_context = {'site_name': SITE_NAME, 'rate_articles': rate_articles}
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
    

# Logout page view.
class ALogoutView(LoginRequiredMixin, LogoutView):
    extra_context = {'site_name': SITE_NAME}
    template_name = 'articles/user_actions/logout.html'
    
    def get(self, *args):
        messages.add_message(self.request, messages.SUCCESS, 'Вы успешно вышли с сайта!')
        return redirect(reverse_lazy('articles:index'))
    
    
# Register page view.
class ARegisterUserView(CreateView):
    model = AdvUser
    template_name = 'articles/user_actions/register_user.html'
    form_class = ARegisterUserForm
    success_url = reverse_lazy('articles:register_done')
    
    def get(self, request):
        return render(request, self.template_name, {'site_name': SITE_NAME})
    
    
# When user activated.
class ARegisterDoneView(TemplateView):
    template_name = 'articles/user_actions/register_done.html'
    
    def get(self, request):
        return render(request, self.template_name, {'site_name': SITE_NAME})
 

# Change info view.
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    
    model = AdvUser
    template_name = 'articles/user_actions/change_user_info.html'
    form_class = ChangeUserInfoForm
    
    def dispatch(self, request, username, *args, **kwargs):
        self.user = get_object_or_404(AdvUser, username=username)
        self.user_id = self.user.pk
        self.success_url = reverse_lazy('articles:profile', kwargs={'username': self.user.username})
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, username=self.user.username)
    
    def get(self, request):
        form = ChangeUserInfoForm(instance=self.user)
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = ChangeUserInfoForm(request.POST, request.FILES, instance=self.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Профиль успешно отредактирован.')
        else:
            messages.add_message(request, messages.WARNING, 'Произошла ошибка при изменении данных профиля.')
        return redirect('articles:profile', username=self.user.username)


# Change password.
class APasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'articles/user_actions/change_password.html'
    success_url = reverse_lazy('articles:profile')
    success_message = 'Пароль успешно изменен.'


# Forget password.
class APasswordResetView(PasswordResetView):
    template_name = 'articles/user_actions/reset_password.html'
    subject_template_name = 'email/reset_password_letter_subject.txt'
    email_template_name = 'email/reset_password_letter_body.txt'
    success_url = reverse_lazy('articles:reset_password_done')


class APasswordResetDoneView(SuccessMessageMixin, PasswordResetDoneView):
    template_name = 'articles/user_actions/reset_password_done.html'
    success_message = 'Письмо успешно отправлено!'


class APasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'articles/user_actions/reset_password_confirm.html'
    success_url = reverse_lazy('articles:reset_password_complete')


class APasswordResetCompleteView(SuccessMessageMixin, PasswordResetCompleteView):
    template_name = 'articles/user_actions/reset_password_complete.html'
    success_message = 'Пароль успешно изменен.'