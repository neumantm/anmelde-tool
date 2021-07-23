# myapi/urls.py
from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'event', views.EventViewSet)
router.register(r'age-group', views.AgeGroupViewSet)
router.register(r'event-location', views.EventLocationViewSet)
router.register(r'scout-hierarchy', views.ScoutHierarchyViewSet)
router.register(r'scout-hierarchy-group', views.ScoutHierachyGroupViewSet, basename="scout-hierarchy-group")
router.register(r'registration', views.RegistrationViewSet, basename='registration')
router.register(r'zip-code', views.ZipCodeViewSet)
router.register(r'participant-group', views.ParticipantGroupViewSet, basename="participant-group")
router.register(r'participant-personal', views.ParticipantPersonalViewSet)
router.register(r'eat-habit-type', views.EatHabitTypeViewSet)
router.register(r'eat-habit', views.EatHabitViewSet)
router.register(r'travel-type', views.TravelTypeViewSet)
router.register(r'travel-tag', views.TravelTagViewSet)
router.register(r'tent-type', views.TentTypeViewSet)
router.register(r'tent', views.TentViewSet)
router.register(r'scout-orga-level', views.ScoutOrgaLevelViewSet)
router.register(r'role', views.RoleViewSet)
router.register(r'method-of-travel', views.MethodOfTravelViewSet)
router.register(r'event-overview', views.EventOverviewViewSet)
router.register(r'check-event', views.EventCodeCheckerViewSet, basename="event-code")
router.register(r'postal-address', views.PostalAddressViewSet)
router.register(r'workshop', views.WorkshopViewSet, basename="workshop")
router.register(r'workshop-stats', views.WorkshopStatsViewSet, basename="workshopStats")

event_router = routers.NestedSimpleRouter(router, r'event', lookup='event')
event_router.register(r'participants', views.EventParticipantsViewSet,
                      basename='event-participants')
event_router.register(r'eventmaster-overview', views.EventMasterViewSet,
                      basename='event-eventmaster-overview')
event_router.register(r'cash-eventmaster-overview', views.EventCashMasterViewSet,
                      basename='cash-event-master-overview')
event_router.register(r'kitchen-eventmaster-overview', views.EventKitchenMasterViewSet,
                      basename='kitchen-event-master-overview')
event_router.register(r'program-eventmaster-overview', views.EventProgramMasterViewSet,
                      basename='program-event-master-overview')
event_router.register(r'xlsx-generator/event_locations_fee', views.EventLocationFeeXlsxViewSet,
                      basename='event_locations_fee')
event_router.register(r'xlsx-generator/travel-preference', views.TravelPreferenceXlsxViewSet,
                      basename='travel-preference')
event_router.register(r'xlsx-generator/text-package-address', views.TextAndPackageAddressXlsxViewSet,
                      basename='text-package-address')
event_router.register(r'xlsx-generator/registration-groups', views.RegistrationGroupsViewSet,
                      basename='registration-groups')
event_router.register(r'registration-stats', views.RegistrationStatViewSet,
                      basename='registration-stats-details')
event_router.register(r'registration-reminder', views.ReminderMailViewSet,
                      basename='registration-reminder-details')

registration_router = routers.NestedSimpleRouter(router, r'registration', lookup='registration')
registration_router.register(r'participants', views.RegistrationParticipantsViewSet, basename='participants')
registration_router.register(r'summary', views.RegistrationSummaryViewSet, basename='summary')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('basic/', include(router.urls)),
    path('basic/', include(event_router.urls)),
    path('basic/', include(registration_router.urls))
]
