from rest_framework import serializers

from favourites.models import Favourites
from foods.models import Foods
from foods.serializers import FoodsSerializer
from phasesDay.models import PhasesDay
from phasesDay.serializers import PhasesDaySerializer
from users.models import User
from users.serializers import UserSerializer


class FavouritesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    foods = FoodsSerializer(read_only=True, many=True)
    phasesDay = PhasesDaySerializer(read_only=True, many=True)

    class Meta:
        model = Favourites
        fields = ('id',
                  'name',
                  'description',
                  'created_at',
                  'updated_at',
                  'user',
                  'foods',
                  'phasesDay')


class UpdateFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = ('id',
                  'name',
                  'description',)


class CreateFavouriteSerializer(serializers.ModelSerializer):
    idUser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    idFoods = serializers.PrimaryKeyRelatedField(queryset=Foods.objects.all(), many=True, write_only=True)
    idPhasesDay = serializers.PrimaryKeyRelatedField(queryset=PhasesDay.objects.all(), many=True, write_only=True)
    user = UserSerializer(read_only=True)
    foods = FoodsSerializer(read_only=True, many=True)
    phasesDay = PhasesDaySerializer(read_only=True, many=True)

    class Meta:
        model = Favourites
        fields = ('name',
                  'description',
                  'created_at',
                  'updated_at',
                  'user',
                  'foods',
                  'phasesDay',
                  'idUser',
                  'idFoods',
                  'idPhasesDay',)

    def create(self, validated_data):
        user = validated_data.pop('idUser')
        foods = validated_data.pop('idFoods')
        phases_day = validated_data.pop('idPhasesDay')

        current_user = user if user is not None else self.context.get('request').user

        instance = Favourites.objects.create(
            user=current_user,
            **validated_data)

        instance.foods.set(foods)
        instance.phasesDay.set(phases_day)
        return instance
