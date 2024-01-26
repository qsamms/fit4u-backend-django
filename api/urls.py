from django.urls import path
from .views import user_views

urlpatterns = [
     path('user/', user_views.UserAPI.as_view()),
]