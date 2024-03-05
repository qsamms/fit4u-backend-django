from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Meta:
        app_label = "api"

    email = models.EmailField(null=False, unique=True)
    is_oauth = models.BooleanField(null=False, blank=False, default=False)
    UNIT_CHOICES = [
        ("lbs", "lbs"),
        ("kg", "kg"),
    ]
    pref_unit = models.CharField(max_length=150, default="lbs", choices=UNIT_CHOICES)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]
