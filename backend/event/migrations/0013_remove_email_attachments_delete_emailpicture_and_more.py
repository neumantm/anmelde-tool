# Generated by Django 4.0.3 on 2022-03-27 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0012_event_invitation_code_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='attachments',
        ),
        migrations.DeleteModel(
            name='EmailPicture',
        ),
        migrations.DeleteModel(
            name='Email',
        ),
        migrations.DeleteModel(
            name='EmailAttachment',
        ),
    ]
