from rest_framework import serializers

from foods.models import Foods
from foods.serializers import FoodsSerializer
from users.models import User
from users.serializers import UserSerializer
from .models import Records


class RecordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    foods = FoodsSerializer(read_only=True, many=True)

    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'user',
                  'foods',
                  'date',)


class UpdateRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'date',)


class FullRecordSerializer(serializers.ModelSerializer):
    foods = FoodsSerializer(many=True)

    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'foods',
                  'date',)


class CreateRecordSerializer(serializers.ModelSerializer):
    idUser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    idFoods = serializers.PrimaryKeyRelatedField(queryset=Foods.objects.all(), many=True, write_only=True)
    user = UserSerializer(read_only=True)
    foods = FoodsSerializer(many=True, read_only=True)

    class Meta:
        model = Records
        fields = ('blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'idUser',
                  'idFoods',
                  'foods',
                  'user',
                  'date')

    def create(self, validated_data):
        user = validated_data.pop('idUser')
        foods = validated_data.pop('idFoods')
        current_user = user if user is not None else self.context.get('request').user

        instance = Records.objects.create(
            user=current_user,
            **validated_data)

        instance.foods.set(foods)
        return instance
