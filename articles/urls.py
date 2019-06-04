from django.urls import path

from .views import index, detail, profile
from .views import ALoginView, ALogoutView, ARegisterUserView
from .views import ARegisterDoneView, user_activate, ChangeUserInfoView
from .views import ArticleAddView, change_rating, ArticleDeleteView
from .views import ArticleEditView, APasswordChangeView, APasswordResetView
from .views import APasswordResetDoneView, APasswordResetConfirmView
from .views import APasswordResetCompleteView, subscribe, unsubscribe
from .views import search_by_tag

app_name = 'articles'
urlpatterns = [
    path('accounts/profile/unsubscribe/<str:username>/', unsubscribe, name='unsubscribe'),
    path('accounts/profile/subscribe/<str:username>/', subscribe, name='subscribe'),
    path('accounts/password/reset/complete/', APasswordResetCompleteView.as_view(), name='reset_password_complete'),
    path('accounts/password/reset/confirm/<uidb64>/<token>/', APasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('accounts/password/reset/done/', APasswordResetDoneView.as_view(), name='reset_password_done'),
    path('accounts/password/reset/', APasswordResetView.as_view(), name='reset_password'),
    path('accounts/password/change/', APasswordChangeView.as_view(), name='change_password'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', ARegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', ARegisterUserView.as_view(), name='register'),
    path('accounts/profile/edit/<int:pk>/', ArticleEditView.as_view(), name='edit_article'),
    path('accounts/profile/delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete_article'),
    path('accounts/profile/add/', ArticleAddView.as_view(), name='add_article'),
    path('accounts/profile/change/<str:username>', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/<str:username>/', profile, name='profile'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', ALogoutView.as_view(), name='logout'),
    path('accounts/login/', ALoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('articles/search/<str:tag>/', search_by_tag, name='search'),
    path('articles/<int:pk>/<int:rating>/', change_rating, name='change_rating'),
    path('articles/<int:pk>/', detail, name='article'),
    path('', index, name='index'),
]
