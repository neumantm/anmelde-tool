# Generated by Django 3.1.4 on 2021-01-24 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_auto_20210120_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participantpersonal',
            name='date_birth',
        ),
        migrations.AddField(
            model_name='participantpersonal',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
