# Generated by Django 4.0.3 on 2022-03-20 15:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtended',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mobile_number', models.CharField(blank=True, max_length=20)),
                ('scout_name', models.CharField(blank=True, max_length=20)),
                ('dsgvo_confirmed', models.BooleanField(default=False)),
                ('email_notifaction', models.CharField(choices=[('Full', 'Full'), ('Daily', 'Daily'), ('Important', 'Important')], default='Full', max_length=10)),
                ('sms_notifcation', models.BooleanField(default=True)),
            ],
        ),
    ]
