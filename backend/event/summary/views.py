from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q
from rest_framework import mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from basic.models import ScoutHierarchy
from basic.serializers import ScoutHierarchySerializer
from event import models as event_models
from event import permissions as event_permissions
from event.helper import filter_registration_by_leadership, get_bund, to_snake_case, get_event, age_range, \
    filter_registrations_by_query_params
from event.summary import serializers as summary_serializers

User = get_user_model()


class WorkshopEventSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson | event_permissions.IsLeaderPerson]
    serializer_class = summary_serializers.WorkshopEventSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        event: event_models.Event = get_event(event_id)

        workshops = event_models.Workshop.objects.filter(registration__event__id=event_id)

        if not event_permissions.check_event_permission(event, self.request.user) \
                and event_permissions.check_leader_permission(event, self.request.user):
            bund = get_bund(self.request.user.userextended.scout_organisation)
            workshops = workshops.filter(Q(registration__scout_organisation__parent=bund)
                                         | Q(registration__scout_organisation__parent__parent=bund)
                                         | Q(registration__scout_organisation__parent__parent__parent=bund)
                                         | Q(registration__scout_organisation__parent__parent__parent__parent=bund))
        return workshops


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page-size'
    max_page_size = 1000
    page_size = 1000


class EventSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson | event_permissions.IsLeaderPerson]
    serializer_class = summary_serializers.RegistrationEventSummarySerializer
    ordering_fields = ('scout_organisation__name', 'is_confirmed', 'single', 'created_at', 'updated_at')
    pagination_class = StandardResultsSetPagination

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        registrations = event_models.Registration.objects.filter(event=event_id)

        registrations = filter_registrations_by_query_params(self.request, event_id, registrations)

        ordering: str = self.request.query_params.get('ordering', None)
        order_desc: bool = self.request.query_params.get('order-desc', 'false') == 'true'
        camel_case = to_snake_case(ordering, order_desc, self.ordering_fields)

        return registrations.order_by(camel_case)


class RegistrationLocationViewSet(EventSummaryViewSet):
    pagination_class = None
    serializer_class = summary_serializers.RegistrationLocationSerializer


class EventLocationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson | event_permissions.IsLeaderPerson]
    serializer_class = summary_serializers.EventLocationSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.Event.objects.filter(id=event_id)


class EventDetailedSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventSuperResponsiblePerson | event_permissions.IsLeaderPerson]
    serializer_class = summary_serializers.RegistrationParticipantEventDetailedSummarySerializer
    ordering_fields = ('first_name', 'last_name', 'scout_name', 'birthday', 'scout_organisation')
    pagination_class = StandardResultsSetPagination

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        registrations = event_models.Registration.objects.filter(event=event_id)
        registrations = filter_registrations_by_query_params(self.request, event_id, registrations)

        reg_ids = registrations.values_list('id', flat=True)

        participants: QuerySet = event_models.RegistrationParticipant.objects.filter(registration__id__in=reg_ids)

        booking_option_list = self.request.query_params.getlist('booking-option')
        if booking_option_list:
            participants = participants.filter(booking_option__in=booking_option_list)

        ordering: str = self.request.query_params.get('ordering', None)
        order_desc: bool = self.request.query_params.get('order-desc', 'false') == 'true'
        camel_case = to_snake_case(ordering, order_desc, self.ordering_fields, 'last_name')

        check_case = ('-' if order_desc else '') + 'scout_organisation'
        if camel_case == check_case:
            camel_case = ('-' if order_desc else '') + 'registration__scout_organisation__name'

        return participants.order_by(camel_case)


class EventAttributeSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.EventAttributeSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        mapper_ids = event_models.EventModuleMapper.objects.filter(event=event_id).values_list('attributes', flat=True)
        return event_models.AttributeEventModuleMapper.objects.filter(id__in=mapper_ids)


class EventFoodSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson | event_permissions.IsLeaderPerson]

    def list(self, request, *args, **kwargs) -> Response:
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

        registrations = event_models.Registration.objects.filter(event=event_id)
        registrations = filter_registrations_by_query_params(self.request, event_id, registrations)

        registration_ids = registrations.values_list('id', flat=True)

        queryset = event_models.RegistrationParticipant.objects.filter(registration__id__in=registration_ids)

        booking_option_list = self.request.query_params.getlist('booking-option')
        if booking_option_list:
            queryset = queryset.filter(booking_option__in=booking_option_list)

        return queryset


class EventLeaderTypesSummaryViewSet(EventFoodSummaryViewSet):

    def list(self, request, *args, **kwargs) -> Response:
        all_participants: QuerySet[event_models.RegistrationParticipant] = self.get_queryset()

        n = self.get_leder_type_count('N', all_participants)
        staFue = self.get_leder_type_count('StaFue', all_participants)
        siFue = self.get_leder_type_count('SiFue', all_participants)
        roFue = self.get_leder_type_count('RoFue', all_participants)
        meuFue = self.get_leder_type_count('MeuFue', all_participants)

        result = {
            'n': n,
            'staFue': staFue,
            'siFue': siFue,
            'roFue': roFue,
            'meuFue': meuFue,
        }

        return Response(result, status=status.HTTP_200_OK)

    def get_leder_type_count(self, leader_type, participants: QuerySet[event_models.RegistrationParticipant]):
        return participants.filter(leader=leader_type).count()


class EventAgeGroupsSummaryViewSet(EventFoodSummaryViewSet):

    def list(self, request, *args, **kwargs) -> Response:
        """
        0-10 Wölfling
        11-16 Pfadfinder
        17-23 Rover
        23+ Altrover
        """
        event_id = self.kwargs.get("event_pk", None)
        event = get_event(event_id)
        all_participants: QuerySet[event_models.RegistrationParticipant] = self.get_queryset()

        woelfling = age_range(0, 13, all_participants, event)
        pfadfinder = age_range(13, 18, all_participants, event)
        rover = age_range(18, 25, all_participants, event)
        alt_rover = age_range(25, 999, all_participants, event)

        result = {
            'woelfling': woelfling,
            'pfadfinder': pfadfinder,
            'rover': rover,
            'alt_rover': alt_rover
        }

        return Response(result, status=status.HTTP_200_OK)


class EventAlcoholAgeGroupsSummaryViewSet(EventFoodSummaryViewSet):

    def list(self, request, *args, **kwargs) -> Response:
        event_id = self.kwargs.get("event_pk", None)
        event = get_event(event_id)
        all_participants: QuerySet[event_models.RegistrationParticipant] = self.get_queryset()

        young = age_range(0, 16, all_participants, event)
        teen = age_range(16, 18, all_participants, event)
        adult = age_range(18, 999, all_participants, event)

        result = {
            'child': young,
            'teen': teen,
            'adult': adult
        }

        return Response(result, status=status.HTTP_200_OK)


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
        only_admin = self.request.query_params.get('only-admins', False)
        event: event_models.Event = event_models.Event.objects.filter(id=event_id).first()

        all_users: QuerySet[User] = event.responsible_persons.exclude(email__exact='')

        if event.keycloak_admin_path:
            admin_groups: QuerySet[User] = event.keycloak_admin_path.user_set.exclude(email__exact='')
            all_users = admin_groups | all_users

        if not only_admin and event.keycloak_path:
            normal_groups: QuerySet[User] = event.keycloak_path.user_set.exclude(email__exact='')
            all_users = all_users | normal_groups

        return all_users.distinct()


class EmailRegistrationResponsiblePersonsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.UserEmailSerializer

    def get_queryset(self) -> QuerySet[User]:
        event_id = self.kwargs.get("event_pk", None)

        confirmed: bool = self.request.query_params.get('confirmed', 'true') == 'true'
        unconfirmed: bool = self.request.query_params.get('unconfirmed', 'true') == 'true'
        # all_participants: bool = self.request.query_params.get('all-participants', False)

        all_registrations: QuerySet[event_models.Registration] = event_models.Registration.objects. \
            filter(event=event_id)
        registrations: QuerySet[event_models.Registration] = event_models.Registration.objects.none()

        if confirmed:
            confirmed_registrations = all_registrations.filter(is_confirmed=True)
            registrations = registrations | confirmed_registrations

        if unconfirmed:
            unconfirmed_registrations = all_registrations.filter(is_confirmed=False)
            registrations = registrations | unconfirmed_registrations

        registrations_ids: QuerySet[int] = registrations.all().distinct() \
            .values_list('responsible_persons__id', flat=True)
        all_users = User.objects.filter(id__in=registrations_ids).distinct().exclude(email__exact='')

        return all_users


class RegistrationParentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson | event_permissions.IsLeaderPerson]
    serializer_class = ScoutHierarchySerializer

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk", None)
        level_id = self.request.query_params.get('level', 5)

        registrations = event_models.Registration.objects.filter(event=event_id)
        registrations = filter_registration_by_leadership(self.request.user, event_id, registrations)
        ids = registrations.values_list('scout_organisation__id', flat=True)

        return ScoutHierarchy.objects.filter(Q(id__in=ids) |
                                             Q(parent__id__in=ids) |
                                             Q(parent__parent__id__in=ids) |
                                             Q(parent__parent__parent__id__in=ids),
                                             level__id=level_id).distinct().order_by('name')
