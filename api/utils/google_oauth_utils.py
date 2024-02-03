# services.py
from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from urllib.parse import urlencode
from typing import Dict, Any
import requests
from api.models import CustomUser


GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://accounts.google.com/o/oauth2/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
REVOKE_TOKEN_URL = "https://accounts.google.com/o/oauth2/revoke"

LOGIN_URL = f"{settings.BASE_APP_URL}/login"


# Exchange authorization token with access token
def google_get_access_token(code: str, redirect_uri: str) -> str:
    data = {
        "code": code,
        "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
        "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
    if not response.ok:
        print(response.json())
        raise ValidationError("Could not get access token from Google.")

    access_token = response.json()["access_token"]

    return access_token


# Get user info from google
def google_get_user_info(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if not response.ok:
        raise ValidationError("Could not get user info from Google.")

    return response.json()


def get_or_create_user(validated_data):
    domain = settings.BASE_API_URL
    redirect_uri = f"{domain}/api/auth/login/google/"

    code = validated_data.get("code")
    error = validated_data.get("error")

    if error or not code:
        params = urlencode({"error": error})
        return redirect(f"{LOGIN_URL}?{params}")

    access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
    user_data = google_get_user_info(access_token=access_token)

    # Creates user in DB if first time login
    return CustomUser.objects.get_or_create(
        email=user_data["email"],
        username=user_data["email"],
        first_name=user_data.get("given_name"),
        last_name=user_data.get("family_name"),
        is_oauth=True,
    )
