from rest_framework_simplejwt.views import TokenRefreshView
from user import views
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup_for_client, name='signup_for_client'),
    path('signup-operator/', views.signup_for_operator,
         name='signup_for_operator'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
