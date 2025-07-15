from django.urls import path
from .views import RegisterView
from dj_rest_auth.views import LogoutView

from apiconf.views import UserFinancesView, CustomLoginView, CustomUserDetailsView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='login'),
    path('user/', CustomUserDetailsView.as_view(), name='user'),
    path('user/finances/', UserFinancesView.as_view(), name='user-finances'),
]