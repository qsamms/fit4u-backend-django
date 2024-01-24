from django.urls import path
from .views import google_oauth

urlpatterns = [
    path('auth/login/google/', google_oauth.google_login_api),
]