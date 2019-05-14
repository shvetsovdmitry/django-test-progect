from django.urls import path

from .views import index, detail, profile
from .views import ALoginView, ALogoutView, ARegisterUserView
from .views import ARegisterDoneView, user_activate

app_name = 'articles'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', ARegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', ARegisterUserView.as_view(), name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', ALogoutView.as_view(), name='logout'),
    path('accounts/login/', ALoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('articles/<int:pk>/', detail, name='article'),
    path('', index, name='index'),
]
