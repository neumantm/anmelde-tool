# Generated by Django 3.2.9 on 2021-11-28 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TagTime',
            new_name='TimeAttribute',
        ),
    ]
