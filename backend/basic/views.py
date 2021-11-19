import io
import time
from django.contrib.auth.models import User
from django.db.models import Q, Case, When, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from helper.user_creation import CreateUserExternally
from rest_framework.response import Response
from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, \
    ZipCode, ParticipantGroup, Role, MethodOfTravel, Tent, \
    ScoutOrgaLevel, ParticipantPersonal, EatHabitType, EatHabit, TravelType, \
    TentType, EatHabit, TravelTag, PostalAddress, EventRoleMapping, RegistrationMatching, \
    Workshop, EventTag, Contact
from .serializers import EventSerializer, AgeGroupSerializer, EventLocationSerializer, \
    ScoutHierarchySerializer, RegistrationSerializer, ZipCodeSerializer, ParticipantGroupSerializer, \
    RoleSerializer, MethodOfTravelSerializer, TentSerializer, \
    EventParticipantsSerializer, ScoutOrgaLevelSerializer, ParticipantPersonalSerializer, \
    EatHabitTypeSerializer, EatHabitSerializer, TravelTypeSerializer, \
    TentTypeSerializer, EventOverviewSerializer, EatHabitSerializer, EventCashMasterSerializer, \
    EventKitchenMasterSerializer, EventProgramMasterSerializer, RegistrationParticipantsSerializer, \
    RegistrationSummarySerializer, TravelTagSerializer, PostalAddressSerializer, RegistrationStatSerializer, \
    WorkshopSerializer, WorkshopStatsSerializer, SimpleMailSerializer, EventTagSerializer, ContactSerializer

from .permissions import IsEventMaster, IsKitchenMaster, IsEventCashMaster, IsProgramMaster, \
    IsLogisticMaster, IsSocialMediaPermission, IsResponsiblePersonPermission, IsTeamMemberPermission, \
    IsOrganisationLeader, IsResponsiblePersonParticipantPersonalPermission

from helper.registration_summary import registration_responsible_person, create_registration_summary, \
    create_reminder_registration
from helper.registration_matching_mail import create_matching_mail
import helper.email


def get_dataset(kwargs, pk, dataset):
    dataset_id = kwargs.get(pk, None)
    if dataset_id is not None:
        return dataset.objects.filter(id=dataset_id)
    else:
        return Response('No dataset selected', status=status.HTTP_400_BAD_REQUEST)


def get_event(kwargs):
    event_id = kwargs.get("event_pk", None)
    if event_id is not None:
        return Event.objects.filter(id=event_id)
    else:
        return Response('No event selected', status=status.HTTP_400_BAD_REQUEST)


def filter_data(user, kwargs, data):
    event_id = kwargs.get("event_pk", None)
    role = EventRoleMapping.objects.filter(event_id=event_id, user=user)
    # parent_level =
    # queryset = data.objects.filter()
    return


def get_registrations_from_event(kwargs):
    event_id = kwargs.get("event_pk", None)
    if event_id is not None:
        return Registration.objects.filter(event=event_id)
    else:
        return Response('No event selected', status=status.HTTP_400_BAD_REQUEST)


def create_missing_eat_habit(request):
    # Check whether habit type exists
    if 'eat_habit_type' in request.data:
        habit_types = request.data['eat_habit_type']
        for food_type in habit_types:
            if not EatHabitType.objects.filter(name__exact=food_type).exists():
                new_type = EatHabitType.objects.create(name=food_type)
                new_type.save()


def create_missing_scout_group(request):
    # Check whether group name exits
    if 'scout_group' in request.data:
        scout_group = request.data['scout_group']
        if not ScoutHierarchy.objects.filter(name__exact=scout_group, level__id=6).exists():
            new_group = ScoutHierarchy.objects.create(name=scout_group, level=ScoutOrgaLevel.objects.get(pk=6),
                                                      parent=request.user.userextended.scout_organisation)
            new_group.save()


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventOverviewViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventOverviewSerializer


class AgeGroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer


class EventLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('registration',)
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer


class ScoutHierarchyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ScoutHierarchy.objects.all().exclude(level=6)
    serializer_class = ScoutHierarchySerializer


class ScoutHierachyGroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoutHierarchySerializer

    def get_queryset(self):
        return ScoutHierarchy.objects.filter(level=6, parent=self.request.user.userextended.scout_organisation)


class RegistrationViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'default': [IsAuthenticated, IsResponsiblePersonPermission]}
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id',)

    def create(self, request, *args, **kwargs):
        if 'event' not in request.data:
            return Response('Event not selected', status=status.HTTP_400_BAD_REQUEST)
        # Check invitation code
        queryset_event = Event.objects.all()
        event = get_object_or_404(queryset_event, pk=request.data['event'])

        if request.user.userextended.scout_organisation.id != request.data['scout_organisation']:
            return Response({'forbidden': 'scout organisation from user and request does not match'},
                            status=status.HTTP_403_FORBIDDEN)
        if event.registration_set.filter(scout_organisation=request.user.userextended.scout_organisation.id).exists():
            return Response({'forbidden': 'already registered'}, status=status.HTTP_403_FORBIDDEN)

        if 'code' in self.request.query_params:
            code = self.request.query_params.get('code', None)
        else:
            return Response({'code': 'missing query param'}, status=status.HTTP_400_BAD_REQUEST)

        if event.invitation_code != code:
            raise PermissionDenied('wrong invitation code')

        self.add_responsible_person(event, request)

        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, partial=False):
        queryset_registration = Registration.objects.all()
        registration = get_object_or_404(queryset_registration, pk=pk)

        if "responsible_persons" in request.data or not partial:
            queryset_event = Event.objects.all()
            event = get_object_or_404(queryset_event, pk=request.data['event'])
            self.add_responsible_person(event, request, registration)

        response = super().update(request, pk, partial=partial)

        if registration is not None and not registration.is_confirmed and 'is_confirmed' in response.data and \
                response.data['is_confirmed']:
            create_registration_summary(response.data)
        return response

    def add_responsible_person(self, event, request, registration=None):
        event_data = {'event': event.name,
                      'event_id': event.id,
                      'foreign_email': request.user.username,
                      'foreign_name': request.user.userextended.scout_name
                      }

        # Check responsible person
        emails = request.data['responsible_persons']

        # Check if responsible person already exists
        new_responsible_persons = []
        if registration is not None:
            existing_responsible_persons = registration.responsible_persons.values_list('username', flat=True)

            for email in emails:
                if email not in existing_responsible_persons:
                    new_responsible_persons.append(email)
        else:
            new_responsible_persons = emails

        # send to each new responsible person a notification
        for user_email in new_responsible_persons:
            if user_email != request.user.username:
                data = event_data
                user = User.objects.filter(username=user_email).first()
                if user is None:
                    data.update(CreateUserExternally(user_email, event_data))
                else:
                    user_data = {'username': user.userextended.scout_name if user.userextended is not None else
                    user.username.split('@', 1)[0],
                                 'user': user.username,
                                 'email': user.username,
                                 }
                    data.update(user_data)
                registration_responsible_person(data)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes_by_action['default']]


class ZipCodeSearchFilter(FilterSet):
    zip_city = CharFilter(field_name='zip_city', method='get_zip_city')

    class Meta:
        model = ZipCode
        fields = ['zip_code', 'city', 'id']

    def get_zip_city(self, queryset, field_name, value):
        cities = queryset.filter(Q(zip_code__contains=value) | Q(city__contains=value))
        if cities.count() > 250:
            raise PermissionDenied('Too many results!!!')
        return cities


class ZipCodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ZipCode.objects.all()
    serializer_class = ZipCodeSerializer
    filterset_class = ZipCodeSearchFilter


class ParticipantGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ParticipantGroup.objects.all().order_by('-updated_at')
    serializer_class = ParticipantGroupSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('registration',)


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class MethodOfTravelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MethodOfTravel.objects.all()
    serializer_class = MethodOfTravelSerializer


class TentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tent.objects.all()
    serializer_class = TentSerializer


class ScoutOrgaLevelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ScoutOrgaLevel.objects.all()
    serializer_class = ScoutOrgaLevelSerializer


class ParticipantPersonalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsResponsiblePersonParticipantPersonalPermission]
    queryset = ParticipantPersonal.objects.all()
    serializer_class = ParticipantPersonalSerializer

    def create(self, request, *args, **kwargs):
        create_missing_scout_group(request)
        create_missing_eat_habit(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        create_missing_scout_group(request)
        create_missing_eat_habit(request)
        return super().update(request, *args, **kwargs)


class EatHabitTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EatHabitType.objects.all()
    serializer_class = EatHabitTypeSerializer


class EatHabitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EatHabit.objects.all()
    serializer_class = EatHabitSerializer

    def create(self, request, *args, **kwargs):
        create_missing_eat_habit(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class TravelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TravelType.objects.all()
    serializer_class = TravelTypeSerializer


class TentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TentType.objects.all()
    serializer_class = TentTypeSerializer


class PostalAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PostalAddress.objects.all()
    serializer_class = PostalAddressSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('registration',)


class TravelTagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TravelTag.objects.all()
    serializer_class = TravelTagSerializer


class EventTagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EventTag.objects.all()
    serializer_class = EventTagSerializer


class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('registration',)


class EventCodeCheckerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)

        if 'code' in self.request.query_params:
            code = self.request.query_params.get('code', None)
        else:
            return Response({'code': 'missing query param'}, status=status.HTTP_400_BAD_REQUEST)

        if event.invitation_code == code:
            return Response({'status': 'Code correct'}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied('wrong invitation code')


class EventMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsEventMaster]
    serializer_class = EventCashMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventCashMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsEventCashMaster]
    serializer_class = EventCashMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventKitchenMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsKitchenMaster]
    serializer_class = EventKitchenMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventProgramMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsProgramMaster]
    serializer_class = EventProgramMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventParticipantsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsTeamMemberPermission]
    serializer_class = EventParticipantsSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class RegistrationParticipantsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsResponsiblePersonPermission]
    serializer_class = RegistrationParticipantsSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("registration_pk", None)
        if event_id is not None:
            return Registration.objects.filter(id=event_id)
        else:
            return Response('No registration selected', status=status.HTTP_400_BAD_REQUEST)


class RegistrationSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsResponsiblePersonPermission]
    serializer_class = RegistrationSummarySerializer

    def get_queryset(self):
        return get_dataset(self.kwargs, 'registration_pk', Registration)


class RegistrationStatViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTeamMemberPermission]  # IsOrganisationLeader
    serializer_class = RegistrationStatSerializer

    def get_queryset(self):
        queryset = get_registrations_from_event(self.kwargs)
        return queryset


class WorkshopViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('registration',)


class WorkshopStatsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkshopStatsSerializer

    def get_queryset(self):
        queryset = get_registrations_from_event(self.kwargs)

        return queryset
