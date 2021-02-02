from .email import send_responsible_person_mail, send_registration_summary
from basic.serializers import RegistrationSummarySerializer
from basic.models import Registration
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict


def registration_responsible_person(data):
    send_responsible_person_mail(data)


def create_registration_summary(data):
    RegistrationSerializer = RegistrationSummarySerializer()
    registration = get_object_or_404(Registration, pk=data['id'])
    total_participants = RegistrationSerializer.get_total_participants(obj=registration)
    total_fee = RegistrationSerializer.get_total_fee(obj=registration)

    for person in registration.responsible_persons.all():
        result = {
            'responsible_person': person.userextended.scout_name if person.userextended.scout_name is not None else person.username,
            'end_date': registration.event.end_time.date(),
            'scout_organisation': registration.scout_organisation,
            'event': registration.event.name,
            'event_id': registration.event.id,
            'responsible_persons': list(registration.responsible_persons.all().values_list('username', flat=True)),
            'total_participants': total_participants,
            'total_fee': total_fee,
            'email': person.username
        }
        send_registration_summary(result)
