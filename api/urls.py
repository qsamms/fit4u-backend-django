from django.urls import path, include
from .views.google_login import GoogleLoginApi

urlpatterns = [
    path('auth/login/google/', GoogleLoginApi.as_view(), name='google_oauth')
]