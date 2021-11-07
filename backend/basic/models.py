from django.db import models
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class ZipCode(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    zip_code = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=60, blank=True)
    lat = models.DecimalField(max_digits=20, decimal_places=15, default=0.000)
    lon = models.DecimalField(max_digits=20, decimal_places=15, default=0.000)

    def __str__(self):
        return self.zip_code + ' - ' + self.city

    def __repr__(self):
        return self.__str__()


class EventLocationType(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class EventLocation(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True)
    location_type = models.ForeignKey(EventLocationType, on_delete=models.PROTECT, null=True, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    address = models.CharField(max_length=60, blank=True)
    contact_name = models.CharField(max_length=30, blank=True)
    contact_email = models.CharField(max_length=30, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    registration = models.ForeignKey("Registration", on_delete=models.PROTECT, null=True, blank=True)
    is_public = models.BooleanField(default=0)
    capacity = models.IntegerField(blank=True, null=True)
    per_person_fee = models.FloatField(blank=True, null=True)
    fix_fee = models.FloatField(blank=True, null=True)
    capacity_corona = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class AgeGroup(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Role(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True)
    force_email = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class ScoutOrgaLevel(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class ScoutHierarchy(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    level = models.ForeignKey(ScoutOrgaLevel, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=60, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.PROTECT, related_name='scouthierarchy', blank=True)

    def __str__(self):
        return "{} - {}".format(self.level, self.name)

    def __repr__(self):
        return self.__str__()


class EventTag(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return self.__str__()


class Event(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    location = models.ForeignKey(EventLocation, on_delete=models.PROTECT, null=True, blank=True)
    age_groups = models.ManyToManyField(AgeGroup, blank=True)
    event_tags = models.ManyToManyField(EventTag, blank=True)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registration_deadline = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registration_start = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    participation_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    min_helper = models.IntegerField(blank=True, null=True)
    min_participation = models.IntegerField(blank=True, null=True)
    max_participation = models.IntegerField(blank=True, null=True)
    invitation_code = models.CharField(max_length=20, blank=True)
    max_scout_orga_level = models.ForeignKey(ScoutOrgaLevel, on_delete=models.PROTECT, null=True, blank=True)
    is_public = models.BooleanField(default=0)
    email_id = models.IntegerField(blank=True, default=0)

    # ToDo: add pdf attatchment
    # ToDo: add html description

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class EventRole(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class EventRoleMapping(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    event_role = models.ForeignKey(EventRole, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.event) + ' : ' + str(self.event_role) + ' : ' + str(self.user)

    def __repr__(self):
        return self.__str__()


class Registration(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    scout_organisation = models.ForeignKey(ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    responsible_persons = models.ManyToManyField(User)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, null=True, blank=True)
    free_text = models.TextField(max_length=10000, blank=True, null=True)
    custom_choice = models.IntegerField(default=0)
    is_confirmed = models.BooleanField(default=0)
    is_accepted = models.BooleanField(default=0)

    def __str__(self):
        return "{} - {}".format(self.scout_organisation, self.event)

    def __repr__(self):
        return "{}".format(self.scout_organisation)


class ParticipantGroup(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    number_of_persons = models.IntegerField(blank=True, null=True)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.PROTECT, null=True, blank=True)
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT, null=True, blank=True)
    participant_role = models.ForeignKey(Role, on_delete=models.PROTECT, default=0)

    def __str__(self):
        return "{} - {}".format(self.registration, self.participant_role)

    def __repr__(self):
        return self.__str__()


class Contact(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    scoutname = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.registration, self.scoutname)

    def __repr__(self):
        return self.__str__()


class EatHabitType(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True)
    is_custom = models.BooleanField(default=1)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class ParticipantPersonal(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT, null=True, blank=True)
    scout_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    scout_group = models.ForeignKey(ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_group_leader = models.BooleanField(default=0)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.PROTECT, null=True, blank=True)
    eat_habit_type = models.ManyToManyField(EatHabitType, blank=True)
    participant_role = models.ForeignKey(Role, on_delete=models.PROTECT, default=0)
    email = models.EmailField(null=True)
    birthday = models.DateField(null=True)

    def __str__(self):
        return "{} - {}".format(self.registration, self.first_name)

    def __repr__(self):
        return self.__str__()


class EatHabit(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    eat_habit_type = models.ForeignKey(EatHabitType, on_delete=models.PROTECT, null=True, blank=True)
    participant_group = models.ForeignKey(ParticipantGroup, on_delete=models.PROTECT, null=True, blank=True)
    number_of_persons = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class TravelType(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class TravelTag(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class MethodOfTravel(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT, null=True, blank=True)
    travel_type = models.ForeignKey(TravelType, on_delete=models.PROTECT, null=True, blank=True)
    number_of_persons = models.IntegerField(blank=True, null=True)
    travel_tag = models.ForeignKey(TravelTag, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.registration, self.travel_type)

    def __repr__(self):
        return self.__str__()


class TentType(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Tent(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT, null=True, blank=True)
    tent_type = models.ForeignKey(TentType, on_delete=models.PROTECT, null=True, blank=True)
    used_by_scout_groups = models.ManyToManyField(ScoutHierarchy, blank=True)

    def __str__(self):
        return "{} - {}".format(self.registration, self.used_by_scout_groups)

    def __repr__(self):
        return self.__str__()


class PostalAddress(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    address_addition = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT, null=True, blank=True)


class RegistrationMatching(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    registrations = models.ManyToManyField(Registration)
    sleeping_location = models.ForeignKey(EventLocation, on_delete=models.CASCADE, null=True, blank=True)
    event_location = models.ForeignKey(ZipCode, on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{} - {} - {}".format(self.event, ", ".join(r.scout_organisation.name for r in self.registrations.all()),
                                     self.sleeping_location)


class Workshop(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    title = models.CharField(max_length=100, blank=True)
    free_text = models.CharField(max_length=1000, blank=True)
    costs = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    supervisor = models.ForeignKey(ParticipantPersonal, on_delete=models.PROTECT, null=True)
    registration = models.ForeignKey("Registration", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title
