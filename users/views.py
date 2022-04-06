from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer, UpdateUserSerializer, FullUserSerializer, CreateUserSerializer
from .models import User
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(description='Get paginated list of users.'),
    update=extend_schema(description='Update user data.'),
    partial_update=extend_schema(description='Partially update user data.'),
    destroy=extend_schema(description='Delete a user.'),
    create=extend_schema(description='Create a new user.'),
)
class UserViewSet(mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.CreateModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    serializer_classes_by_action = {
        'update': UpdateUserSerializer,
        'create': CreateUserSerializer,
        'partial_update': UpdateUserSerializer,
        'get_current_user': FullUserSerializer,
        'get_user_by_id': FullUserSerializer,
    }

    permission_classes = (permissions.AllowAny,)

    @action(methods=["get"], detail=False, url_path='(?P<username>[^/.]+)', url_name="user")
    def get_user_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=["get"], detail=False, url_path='me', url_name="me")
    def get_current_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
