from django.urls import path

from .views import index, detail, profile
from .views import ALoginView, ALogoutView, ARegisterUserView

app_name = 'articles'
urlpatterns = [
    # path('accounts/register/done/', , name='register_done'),
    path('accoutns/register/', ARegisterUserView.as_view(), name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accoutns/logout/', ALogoutView.as_view(), name='logout'),
    path('accounts/login/', ALoginView.as_view(), name='login'),
    path('articles/<int:pk>/', detail, name='article'),
    path('', index, name='index'),
]
