from rest_framework import serializers

from phasesDay.models import PhasesDay


class PhasesDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhasesDay
        fields = ('id',
                  'name',
                  'description',
                  'created_at',
                  'updated_at',)


class UpdatePhasesDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhasesDay
        fields = ('id',
                  'name',
                  'description',
                  'created_at',
                  'updated_at',)


class CreatePhasesDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhasesDay
        fields = ('name',
                  'description',
                  'created_at',
                  'updated_at',)
