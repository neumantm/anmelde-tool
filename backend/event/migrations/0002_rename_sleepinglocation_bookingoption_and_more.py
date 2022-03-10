# Generated by Django 4.0.2 on 2022-03-10 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SleepingLocation',
            new_name='BookingOption',
        ),
        migrations.RenameField(
            model_name='registrationparticipant',
            old_name='sleeping_location',
            new_name='booking_option',
        ),
        migrations.AddField(
            model_name='event',
            name='cloud_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='technical_name',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='registrationparticipant',
            name='gender',
            field=models.CharField(choices=[('M', 'Männlich'), ('F', 'Weiblich'), ('D', 'Divers'), ('N', 'Keine Angabe')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='event',
            name='group_registration',
            field=models.CharField(choices=[('N', 'Nicht erlaubt'), ('O', 'Optional'), ('R', 'Erforderlich')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='event',
            name='single_registration',
            field=models.CharField(choices=[('N', 'Nicht erlaubt'), ('A', 'Angefügt'), ('M', 'Gemischt'), ('E', 'Extern')], default='N', max_length=1),
        ),
    ]
