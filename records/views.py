from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions

from records.models import Records
from records.serializers import RecordSerializer, UpdateRecordSerializer, CreateRecordSerializer


@extend_schema_view(
    list=extend_schema(description='Get paginated list of records.'),
    update=extend_schema(description='Update record data.'),
    partial_update=extend_schema(description='Partially update record data.'),
    destroy=extend_schema(description='Delete a record.'),
    create=extend_schema(description='Create a new record.'),
)
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Records.objects.all()
    serializer_class = RecordSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    serializer_classes_by_action = {
        'update': UpdateRecordSerializer,
        'create': CreateRecordSerializer,
        'partial_update': UpdateRecordSerializer,
    }

    permission_classes = (permissions.AllowAny,)

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]
