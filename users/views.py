from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    # @action(methods=["get"], detail=False, url_path='(?P<username>[^/.]+)', url_name="user")
    # def get_user_by_username(self, request, username):
    #     user = get_object_or_404(User, username=username)
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data)

    @action(methods=["get"], detail=False, url_path='me', url_name="me")
    def get_current_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
