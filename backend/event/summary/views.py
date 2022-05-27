from django.db.models import QuerySet
from rest_framework import mixins, viewsets, status
from django.contrib.auth.models import User

from event import permissions as event_permissions
from event.summary import serializers as summary_serializers
from event import models as event_models
from rest_framework.response import Response


class WorkshopEventSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.WorkshopEventSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.Workshop.objects.filter(registration__event__id=event_id)


class EventSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.EventSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.Event.objects.filter(id=event_id)


class EventDetailedSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventSuperResponsiblePerson]
    serializer_class = summary_serializers.RegistrationParticipantEventDetailedSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        reg_ids = event_models.Registration.objects.filter(event=event_id).values('id')
        booking_option_list = self.request.query_params.getlist('booking-option')

        return event_models.RegistrationParticipant.objects.filter(booking_option__in=booking_option_list).filter(
            registration__in=reg_ids)


class EventAttributeSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.EventAttributeSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        mapper_ids = event_models.EventModuleMapper.objects.filter(event=event_id).values_list('attributes', flat=True)
        return event_models.AttributeEventModuleMapper.objects.filter(id__in=mapper_ids)


class EventFoodSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]

    def list(self, request, *args, **kwargs):
        participants: QuerySet[event_models.RegistrationParticipant] = self.get_queryset()

        eat_habits_sum = {}
        eat_habits = {}
        for participant in participants.all():
            key = tuple(participant.eat_habit.values_list('id', flat=True))
            if key in eat_habits_sum:
                eat_habits_sum[key] += 1
            else:
                eat_habits_sum[key] = 1
                eat_habits[key] = participant.eat_habit.all()

        formatted_eat_habits = []
        for key in eat_habits:
            food = ', '.join(eat_habits[key].values_list('name', flat=True))
            if food is None or food == '':
                food = 'Normal'
            result = {
                'sum': eat_habits_sum[key],
                'food': food,
            }
            formatted_eat_habits.append(result)

        return Response(formatted_eat_habits, status=status.HTTP_200_OK)

    def get_queryset(self) -> QuerySet[event_models.RegistrationParticipant]:
        event_id = self.kwargs.get("event_pk", None)
        booking_option_list = self.request.query_params.getlist('booking-option')
        registration_ids = event_models.Registration.objects.filter(event=event_id, is_confirmed=True) \
            .values_list('id', flat=True)
        queryset = event_models.RegistrationParticipant.objects.filter(registration__id__in=registration_ids)

        if booking_option_list:
            queryset = queryset.filter(booking_option__in=booking_option_list)

        return queryset


class CashSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.CashSummarySerializer

    def get_queryset(self) -> QuerySet[event_models.Event]:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.Event.objects.filter(id=event_id)


class EmailResponsiblePersonsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.UserEmailSerializer

    def get_queryset(self) -> QuerySet[User]:
        event_id = self.kwargs.get("event_pk", None)
        event: event_models.Event = event_models.Event.objects.filter(id=event_id).first()
        admin_groups: QuerySet[User] = event.keycloak_admin_path.user_set.exclude(email__exact='')
        normal_groups: QuerySet[User] = event.keycloak_path.user_set.exclude(email__exact='')
        internal: QuerySet[User] = event.responsible_persons.exclude(email__exact='')
        all_users = admin_groups.union(normal_groups).union(internal)
        return all_users


class EmailRegistrationResponsiblePersonsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.UserEmailSerializer

    def get_queryset(self) -> QuerySet[User]:
        event_id = self.kwargs.get("event_pk", None)
        registrations: QuerySet[int] = event_models.Registration.objects.filter(event=event_id) \
            .values_list('responsible_persons__id', flat=True)
        all_users = User.objects.filter(id__in=registrations).exclude(email__exact='')
        return all_users
