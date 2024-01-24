from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Meta:
        app_label = 'api'
        
    email = models.EmailField(null=False, unique=True)