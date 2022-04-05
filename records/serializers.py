from rest_framework import serializers

from .models import Records


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
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
    idUser = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Records
        fields = ('blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'idUser',
                  'date',)
