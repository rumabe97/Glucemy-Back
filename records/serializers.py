from rest_framework import serializers

from foods.models import Foods
from phasesDay.models import PhasesDay
from users.models import User
from .models import Records


class RecordSerializer(serializers.ModelSerializer):
    # idUser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), read_only=True)
    # idFoods = serializers.PrimaryKeyRelatedField(queryset=Foods.objects.all(), many=True, read_only=True)
    # idPhaseDay = serializers.PrimaryKeyRelatedField(queryset=PhasesDay.objects.all(), read_only=True)

    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'created_date',)
