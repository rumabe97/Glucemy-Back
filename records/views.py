from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions

from records.fullSerializers import UpdateRecordSerializer, CreateRecordSerializer, FullRecordSerializer
from shared.mixins import DynamicSerializersMixin
from records.models import Records
from records.serializers import RecordSerializer


@extend_schema_view(
    list=extend_schema(description='Get paginated list of records.'),
    update=extend_schema(description='Update record data.'),
    partial_update=extend_schema(description='Partially update record data.'),
    destroy=extend_schema(description='Delete a record.'),
    create=extend_schema(description='Create a new record.'),
)
class RecordViewSet(DynamicSerializersMixin, viewsets.ModelViewSet):
    queryset = Records.objects.all()
    serializer_class = RecordSerializer

    serializer_classes_by_action = {
        'update': UpdateRecordSerializer,
        'create': CreateRecordSerializer,
        'partial_update': UpdateRecordSerializer,
        'get_object': FullRecordSerializer,
    }

    permission_classes = (permissions.AllowAny,)
