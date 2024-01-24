from django.conf import *
from django.core.exceptions import ValidationError
import requests

def google_get_access_token(*, code: str, redirect_uri: str) -> str:
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
    data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(settings.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
    if not response.ok:
        raise ValidationError('Failed to obtain access token from Google.')
    
    return response.json()['access_token']

def google_get_user_info(access_token: str) -> dict:
    url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers)

    if response.ok:
        user_data = response.json()
        return user_data
    else: 
        raise ValidationError("Failed to obtain user data from Google.")
        return None