from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from ..utils.google_oauth_utils import *

User = get_user_model()

@api_view(["GET"])
def google_login_api(request): 
    code = request.get("code")
    error = request.get("error")

    if error or not code:
        return Response(data={"error": True}, status=status.HTTP_400_BAD_REQUEST) 

    access_token = google_get_access_token(code=code, redirect_uri="http://localhost:8000/api/auth/login/google")

    user_data = google_get_user_info(access_token=access_token)
    profile = {
        "email": user_data.get("email", ""),
        "first_name": user_data.get("givenName", ""),
        "last_name": user_data.get("familyName", ""),
        "username": user_data.get("username", "")
    }
    user, created = User.objects.get_or_create(**profile) 
    token, created = Token.objects.get_or_create(user=user)
    return Response(data={"token": token.key})





    