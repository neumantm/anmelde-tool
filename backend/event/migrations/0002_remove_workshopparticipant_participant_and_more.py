# Generated by Django 4.0.3 on 2022-04-01 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopparticipant',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='workshopparticipant',
            name='workshop',
        ),
        migrations.DeleteModel(
            name='Workshop',
        ),
        migrations.DeleteModel(
            name='WorkshopParticipant',
        ),
    ]
