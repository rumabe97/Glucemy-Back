from foods.models import Foods
from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema_view, extend_schema
from foods.serializers import FoodsSerializer, UpdateFoodSerializer, CreateFoodSerializer
from shared.mixins import DynamicSerializersMixin, DynamicPermissionsMixin


@extend_schema_view(
    list=extend_schema(description='Get paginated list of foods.'),
    update=extend_schema(description='Update food data.'),
    partial_update=extend_schema(description='Partially update food data.'),
    destroy=extend_schema(description='Delete a food.'),
    create=extend_schema(description='Create a new food.'),
)
class FoodsViewSet(DynamicSerializersMixin, DynamicPermissionsMixin, viewsets.ModelViewSet):
    queryset = Foods.objects.all()
    serializer_class = FoodsSerializer

    serializer_classes_by_action = {
        'update': UpdateFoodSerializer,
        'create': CreateFoodSerializer,
        'partial_update': UpdateFoodSerializer,
    }

    permission_classes_by_action = {
        'create': (permissions.IsAdminUser,),
        'update': (permissions.IsAdminUser,),
        'partial_update': (permissions.IsAdminUser,),
        'destroy': (permissions.IsAdminUser,),
    }
