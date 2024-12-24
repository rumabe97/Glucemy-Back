from django.utils.timezone import now
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from records.models import Records
from shared.mixins import DynamicSerializersMixin, DynamicPermissionsMixin
from shared.permissions import IsOwner
from .fullSerializers import FullUserSerializer
from .serializers import UserSerializer, UpdateUserSerializer
from .models import User
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(description='Get paginated list of users.'),
    update=extend_schema(description='Update user data.'),
    partial_update=extend_schema(description='Partially update user data.'),
    destroy=extend_schema(description='Delete a user.'),
)
class UserViewSet(DynamicSerializersMixin, DynamicPermissionsMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    serializer_classes_by_action = {
        'update': UpdateUserSerializer,
        'partial_update': UpdateUserSerializer,
        'get_current_user': FullUserSerializer,
        'get_user_by_id': FullUserSerializer,
    }

    permission_classes_by_action = {
        'update': (permissions.IsAdminUser | IsOwner,),
        'partial_update': (permissions.IsAdminUser | IsOwner,),
        'destroy': (permissions.IsAdminUser | IsOwner,),
    }

    @action(methods=["get"], detail=False, url_path='get/(?P<username>[^/.]+)', url_name="user")
    def get_user_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=["get"], detail=False, url_path='me', url_name="me")
    def get_current_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(methods=["get"], detail=False, url_path='get_data/glucose', url_name="me")
    def get_last_glucose(self, request):
        latest_record = Records.objects.filter(user=request.user).order_by('-created_date').first()
        if latest_record:
            time_difference = now() - latest_record.created_date
            response = {
                "blood_glucose": latest_record.blood_glucose,
                "created_date": latest_record.created_date,
                "time_since_creation": {
                    "days": time_difference.days,
                    "hours": time_difference.seconds // 3600,
                    "minutes": (time_difference.seconds // 60) % 60
                }
            }
        else:
            response = {
                "error": "No records found"
            }
        return Response(response)
