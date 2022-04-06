from rest_framework import serializers

from foods.models import Foods


class FoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = ('id',
                  'name',
                  'usual_measure',
                  'hc_rations',
                  'glycemic_index',)


class UpdateFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = ('id',
                  'name',
                  'usual_measure',
                  'hc_rations',
                  'glycemic_index',)


class CreateFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = ('name',
                  'usual_measure',
                  'hc_rations',
                  'glycemic_index',)
