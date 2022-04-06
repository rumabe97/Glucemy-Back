from rest_framework import serializers

from users.models import User
from .models import Records


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'user',
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
    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'date',)


class CreateRecordSerializer(serializers.ModelSerializer):
    idUser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Records
        fields = ('blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'idUser',
                  'date',
                  'user')

    def create(self, validated_data):
        user = validated_data.pop('idUser')
        current_user = user if user is not None else self.context.get('request').user

        instance = Records.objects.create(
            user=current_user,
            **validated_data)

        return instance
