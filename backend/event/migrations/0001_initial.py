# Generated by Django 4.0.3 on 2022-04-01 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basic', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('email_services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeEventModuleMapper',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=1000, null=True)),
                ('text', models.CharField(max_length=10000, null=True)),
                ('is_required', models.BooleanField(default=False)),
                ('min_length', models.IntegerField(default=0)),
                ('max_length', models.IntegerField(default=0)),
                ('tooltip', models.CharField(blank=True, max_length=1000, null=True)),
                ('default_value', models.CharField(blank=True, max_length=1000, null=True)),
                ('field_type', models.CharField(blank=True, max_length=25, null=True)),
                ('icon', models.CharField(blank=True, max_length=25, null=True)),
                ('max_entries', models.IntegerField(default=1)),
                ('attribute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.abstractattribute')),
            ],
        ),
        migrations.CreateModel(
            name='BookingOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('bookable_from', models.DateTimeField(blank=True, null=True)),
                ('bookable_till', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('technical_name', models.CharField(blank=True, max_length=15, null=True)),
                ('short_description', models.CharField(blank=True, max_length=100)),
                ('long_description', models.CharField(blank=True, max_length=10000)),
                ('cloud_link', models.CharField(blank=True, max_length=200, null=True)),
                ('event_url', models.CharField(blank=True, max_length=200, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('registration_deadline', models.DateTimeField(blank=True, null=True)),
                ('registration_start', models.DateTimeField(blank=True, null=True)),
                ('last_possible_update', models.DateTimeField(blank=True, null=True)),
                ('invitation_code', models.CharField(blank=True, max_length=20)),
                ('invitation_code_single', models.CharField(blank=True, max_length=20)),
                ('invitation_code_group', models.CharField(blank=True, max_length=20)),
                ('is_public', models.BooleanField(default=False)),
                ('single_registration', models.CharField(choices=[('N', 'Nicht erlaubt'), ('A', 'Angefügt'), ('M', 'Gemischt'), ('E', 'Extern')], default='N', max_length=1)),
                ('group_registration', models.CharField(choices=[('N', 'Nicht erlaubt'), ('O', 'Optional'), ('R', 'Erforderlich')], default='N', max_length=1)),
                ('personal_data_required', models.BooleanField(default=False)),
                ('email_set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='email_services.standardemailregistrationset')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('header', models.CharField(default='Default Header', max_length=100)),
                ('internal', models.BooleanField(default=False)),
                ('custom', models.BooleanField(default=False)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='basic.tagtype')),
            ],
        ),
        migrations.CreateModel(
            name='EventModuleMapper',
            fields=[
                ('ordering', models.IntegerField(auto_created=True, default=999)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('required', models.BooleanField(default=False)),
                ('overwrite_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('standard', models.BooleanField(default=False)),
                ('attributes', models.ManyToManyField(blank=True, to='event.attributeeventmodulemapper')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='event.eventmodule')),
            ],
        ),
        migrations.CreateModel(
            name='EventPlanerModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.tagtype')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_accepted', models.BooleanField(default=False)),
                ('single', models.BooleanField(default=False)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.event')),
                ('responsible_persons', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('scout_organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scouthierarchy')),
                ('tags', models.ManyToManyField(blank=True, to='basic.abstractattribute')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegistrationParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('scout_name', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(default='Generated', max_length=100)),
                ('last_name', models.CharField(default='Generated', max_length=100)),
                ('street', models.CharField(blank=True, max_length=100)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Männlich'), ('F', 'Weiblich'), ('D', 'Divers'), ('N', 'Keine Angabe')], default='N', max_length=1)),
                ('deactivated', models.BooleanField(default=False)),
                ('generated', models.BooleanField(default=False)),
                ('needs_confirmation', models.CharField(choices=[('N', 'Nichts'), ('D', 'Abmelden'), ('AE', 'Anmelden von deaktivierten Teilnehmern'), ('AN', 'Anmelden von neuen Teilnehmern')], default='N', max_length=2)),
                ('leader', models.CharField(choices=[('N', 'Kein Amt'), ('StaFue', 'Stammesführung'), ('SiFue', 'Sippenführung'), ('RoFue', 'Roverrundenführung'), ('MeuFue', 'Meutenführung')], default='N', max_length=6)),
                ('booking_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='event.bookingoption')),
                ('eat_habit', models.ManyToManyField(blank=True, to='basic.eathabit')),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.registration')),
                ('scout_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scouthierarchy')),
                ('tags', models.ManyToManyField(blank=True, to='basic.abstractattribute')),
                ('zip_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.zipcode')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('free_text', models.CharField(blank=True, max_length=1000)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('min_person', models.IntegerField(blank=True, null=True)),
                ('max_person', models.IntegerField(blank=True, null=True)),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.registration')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkshopParticipant',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('participant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event.registrationparticipant')),
                ('workshop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event.workshop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardEventTemplate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event', to='event.event')),
                ('introduction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='introduction', to='event.eventmodulemapper')),
                ('letter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='letter', to='event.eventmodulemapper')),
                ('other_optional_modules', models.ManyToManyField(blank=True, related_name='other_optional_modules', to='event.eventmodulemapper')),
                ('other_required_modules', models.ManyToManyField(blank=True, related_name='other_required_modules', to='event.eventmodulemapper')),
                ('personal_registration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='personal_registration', to='event.eventmodulemapper')),
                ('planer_modules', models.ManyToManyField(blank=True, to='event.eventplanermodule')),
                ('registration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_registration', to='event.eventmodulemapper')),
                ('summary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='confirmation', to='event.eventmodulemapper')),
            ],
        ),
        migrations.CreateModel(
            name='EventLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('address', models.CharField(blank=True, max_length=60)),
                ('contact_name', models.CharField(blank=True, max_length=30)),
                ('contact_email', models.CharField(blank=True, max_length=30)),
                ('contact_phone', models.CharField(blank=True, max_length=30)),
                ('per_person_fee', models.FloatField(blank=True, null=True)),
                ('fix_fee', models.FloatField(blank=True, null=True)),
                ('tags', models.ManyToManyField(blank=True, to='basic.tag')),
                ('zip_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.zipcode')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_planer_modules',
            field=models.ManyToManyField(blank=True, to='event.eventplanermodule'),
        ),
        migrations.AddField(
            model_name='event',
            name='keycloak_admin_path',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='keycloak_admin_group', to='auth.group'),
        ),
        migrations.AddField(
            model_name='event',
            name='keycloak_path',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='keycloak_group', to='auth.group'),
        ),
        migrations.AddField(
            model_name='event',
            name='limited_registration_hierarchy',
            field=models.ForeignKey(default=493, on_delete=django.db.models.deletion.SET_DEFAULT, to='basic.scouthierarchy'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='event.eventlocation'),
        ),
        migrations.AddField(
            model_name='event',
            name='responsible_persons',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, to='basic.tag'),
        ),
        migrations.AddField(
            model_name='event',
            name='theme',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basic.frontendtheme'),
        ),
        migrations.AddField(
            model_name='bookingoption',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event.event'),
        ),
        migrations.AddField(
            model_name='bookingoption',
            name='tags',
            field=models.ManyToManyField(blank=True, to='basic.tag'),
        ),
    ]
