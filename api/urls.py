from django.urls import path, include
from .views.google_login import GoogleLoginApi
from .views.user_views import UserViews

urlpatterns = [
    path('auth/login/google/', GoogleLoginApi.as_view(), name='google_oauth'),
    path('user/me/', UserViews.as_view(), name='get_user'),
]