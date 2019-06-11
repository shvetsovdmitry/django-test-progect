from django.urls import path

from .views import index, detail, profile
from .views import ALoginView, ALogoutView, ARegisterUserView
from .views import ARegisterDoneView, user_activate, ChangeUserInfoView
from .views import ArticleAddView, change_rating, ArticleDeleteView
from .views import ArticleEditView, APasswordChangeView, APasswordResetView
from .views import APasswordResetDoneView, APasswordResetConfirmView
from .views import APasswordResetCompleteView, subscribe_user, unsubscribe_user
from .views import search_by_tag, subscribe_tag, unsubscribe_tag, search_by_category
from .views import subscribe_category, unsubscribe_category, update_user_status

app_name = 'articles'
urlpatterns = [
    path('accounts/profile/unsubscribe/category/<str:category_name>/', unsubscribe_category, name='unsubscribe_category'),
    path('accounts/profile/subscribe/category/<str:category_name>/', subscribe_category, name='subscribe_category'),
    path('accounts/profile/unsubscribe/tag/<str:tag>/', unsubscribe_tag, name='unsubscribe_tag'),
    path('accounts/profile/subscribe/tag/<str:tag>/', subscribe_tag, name='subscribe_tag'),
    path('accounts/profile/unsubscribe/user/<str:username>/', unsubscribe_user, name='unsubscribe_user'),
    path('accounts/profile/subscribe/user/<str:username>/', subscribe_user, name='subscribe_user'),
    path('accounts/password/reset/complete/', APasswordResetCompleteView.as_view(), name='reset_password_complete'),
    path('accounts/password/reset/confirm/<uidb64>/<token>/', APasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('accounts/password/reset/done/', APasswordResetDoneView.as_view(), name='reset_password_done'),
    path('accounts/password/reset/', APasswordResetView.as_view(), name='reset_password'),
    path('accounts/password/change/', APasswordChangeView.as_view(), name='change_password'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', ARegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', ARegisterUserView.as_view(), name='register'),
    path('accounts/profile/updatestatus/', update_user_status, name='update_status'),
    path('accounts/profile/change/<str:username>', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/<str:username>/', profile, name='profile'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', ALogoutView.as_view(), name='logout'),
    path('accounts/login/', ALoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('articles/edit/<int:pk>/', ArticleEditView.as_view(), name='edit_article'),
    path('articles/delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete_article'),
    path('articles/add/', ArticleAddView.as_view(), name='add_article'),
    path('articles/search/category/<str:category_name>/', search_by_category, name='search_by_category'),
    path('articles/search/tag/<str:tag>/', search_by_tag, name='search_by_tag'),
    path('articles/<int:pk>/<int:rating>/', change_rating, name='change_rating'),
    path('articles/<int:pk>/', detail, name='article'),
    path('', index, name='index'),
]
