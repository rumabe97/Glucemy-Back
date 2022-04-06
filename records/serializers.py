from rest_framework import serializers

from foods.models import Foods
from foods.serializers import FoodsSerializer
from phasesDay.models import PhasesDay
from phasesDay.serializers import PhasesDaySerializer
from users.models import User
from users.serializers import UserSerializer
from .models import Records


class RecordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    foods = FoodsSerializer(read_only=True, many=True)
    phasesDay = PhasesDaySerializer(read_only=True)

    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'user',
                  'foods',
                  'phasesDay',
                  'created_date',)


class UpdateRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'created_date',)


class FullRecordSerializer(serializers.ModelSerializer):
    foods = FoodsSerializer(many=True)

    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'foods',
                  'created_date',)


class CreateRecordSerializer(serializers.ModelSerializer):
    idUser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    idFoods = serializers.PrimaryKeyRelatedField(queryset=Foods.objects.all(), many=True, write_only=True)
    idPhaseDay = serializers.PrimaryKeyRelatedField(queryset=PhasesDay.objects.all(), write_only=True)
    user = UserSerializer(read_only=True)
    foods = FoodsSerializer(many=True, read_only=True)
    phasesDay = PhasesDaySerializer(read_only=True)

    class Meta:
        model = Records
        fields = ('blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'idUser',
                  'idFoods',
                  'idPhaseDay',
                  'foods',
                  'user',
                  'phasesDay',
                  'created_date')

    def create(self, validated_data):
        user = validated_data.pop('idUser')
        foods = validated_data.pop('idFoods')
        phases_day = validated_data.pop('idPhaseDay')

        current_user = user if user is not None else self.context.get('request').user

        instance = Records.objects.create(
            user=current_user,
            phasesDay=phases_day,
            **validated_data)

        instance.foods.set(foods)
        return instance
