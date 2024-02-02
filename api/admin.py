from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import *

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(ExternalExercise)
