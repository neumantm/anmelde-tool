# Generated by Django 4.0.2 on 2022-02-06 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0028_rename_responsible_person_event_responsible_persons'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventmodulemapper',
            old_name='position',
            new_name='ordering',
        ),
    ]
