from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions

from favourites.models import Favourites
from favourites.serializers import FavouritesSerializer, UpdateFavouriteSerializer, CreateFavouriteSerializer
from shared.mixins import DynamicSerializersMixin
from shared.permissions import IsOwner


@extend_schema_view(
    list=extend_schema(description='Get paginated list of favourites.'),
    update=extend_schema(description='Update favourite data.'),
    partial_update=extend_schema(description='Partially update favourite data.'),
    destroy=extend_schema(description='Delete a favourite.'),
    create=extend_schema(description='Create a new favourite.'),
)
class FavouritesViewSet(DynamicSerializersMixin, viewsets.ModelViewSet):
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer

    serializer_classes_by_action = {
        'update': UpdateFavouriteSerializer,
        'create': CreateFavouriteSerializer,
        'partial_update': UpdateFavouriteSerializer,
    }

    permission_classes_by_action = {
        'create': (permissions.IsAuthenticated,),
        'update': (permissions.IsAdminUser | IsOwner,),
        'partial_update': (permissions.IsAdminUser | IsOwner,),
        'destroy': (permissions.IsAdminUser | IsOwner,),
    }
