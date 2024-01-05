from rest_framework_simplejwt.views import TokenRefreshView
from user import views
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    # path('login/', views.login, name='login'),
    path('signup/', views.signup_for_client, name='signup_for_client'),
    path('signup-operator/', views.signup_for_operator,
         name='signup_for_operator'),
    path('upload-file/', views.post_file, name="post_file"),
    path('get-file/', views.get_file, name="get_file"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
