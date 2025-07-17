from django.urls import path
from .views import RegisterView, KYCUploadView
from dj_rest_auth.views import LogoutView

from apiconf.views import UserFinancesView, CustomLoginView, CustomUserDetailsView, UserTransactionListView, ChangePasswordView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='login'),
    path('user/', CustomUserDetailsView.as_view(), name='user'),
    path('user/finances/', UserFinancesView.as_view(), name='user-finances'),
    path('user/transactions/', UserTransactionListView.as_view(), name='user-transactions'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('kyc-upload/', KYCUploadView.as_view(), name='kyc'),
]