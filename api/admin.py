from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import *

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'workout', 'set_number', 'external_exercise')
    search_fields = ('name', 'set_number', 'workout__user__email', 'external_exercise__name')

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime')
    search_fields = ('user', 'datetime')

class ExternalExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'muscle', 'equipment', 'difficulty')
    search_fields = ('name', 'type', 'muscle', 'equipment', 'difficulty')

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(ExternalExercise, ExternalExerciseAdmin)
