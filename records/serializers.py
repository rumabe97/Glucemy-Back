from rest_framework import serializers

from .models import Records


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = ('id',
                  'blood_glucose',
                  'carbohydrates',
                  'annotations',
                  'hc_rations',
                  'bolus',
                  'created_date',)


class PDFSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()