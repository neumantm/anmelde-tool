# Generated by Django 4.0.2 on 2022-03-09 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0019_travelattribute'),
        ('event', '0052_rename_description_event_short_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='tags',
            field=models.ManyToManyField(blank=True, to='basic.AbstractAttribute'),
        ),
    ]
