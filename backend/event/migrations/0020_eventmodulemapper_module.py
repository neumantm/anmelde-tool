# Generated by Django 3.2.9 on 2022-01-31 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0019_auto_20220131_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmodulemapper',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='event.eventmodule'),
        ),
    ]
