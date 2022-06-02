from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions, filters

from phasesDay.models import PhasesDay
from phasesDay.serializers import PhasesDaySerializer, UpdatePhasesDaySerializer, CreatePhasesDaySerializer
from shared.mixins import DynamicSerializersMixin, DynamicPermissionsMixin
from shared.permissions import IsOwner


@extend_schema_view(
    list=extend_schema(description='Get paginated list of phases day.'),
    update=extend_schema(description='Update phase day data.'),
    partial_update=extend_schema(description='Partially update phase day data.'),
    destroy=extend_schema(description='Delete a phase day.'),
    create=extend_schema(description='Create a phase day food.'),
)
class PhasesDayViewSet(DynamicSerializersMixin, DynamicPermissionsMixin, viewsets.ModelViewSet):
    queryset = PhasesDay.objects.all()
    serializer_class = PhasesDaySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    serializer_classes_by_action = {
        'update': UpdatePhasesDaySerializer,
        'create': CreatePhasesDaySerializer,
        'partial_update': UpdatePhasesDaySerializer,
    }

    permission_classes_by_action = {
        'create': (permissions.IsAuthenticated,),
        'update': (permissions.IsAdminUser | IsOwner,),
        'partial_update': (permissions.IsAdminUser | IsOwner,),
        'destroy': (permissions.IsAdminUser | IsOwner,),
    }
