# Generated by Django 4.2.1 on 2024-02-03 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_exercise_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_oauth',
            field=models.BooleanField(default=False),
        ),
    ]
