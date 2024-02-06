from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import *


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_oauth",
    )


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "workout", "external_exercise")
    search_fields = (
        "name",
        "set_number",
        "workout__user__email",
        "external_exercise__name",
    )


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("user", "datetime")
    search_fields = ("user", "datetime")


class ExternalExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "muscle", "equipment", "difficulty")
    search_fields = ("name", "type", "muscle", "equipment", "difficulty")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(ExternalExercise, ExternalExerciseAdmin)
