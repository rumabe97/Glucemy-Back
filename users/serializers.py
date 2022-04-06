from rest_framework import serializers

#from records.serializers import RecordSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'weight',
                  'height',
                  'age',
                  'created_date',)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'weight',
                  'height',
                  'age',)


class FullUserSerializer(serializers.ModelSerializer):
    #records = RecordSerializer(many=True)

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email',
                  'weight',
                  'height',
                  'age',
                  'first_name',
                  'last_name',
                  'created_date')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'weight',
                  'height',
                  'age',
                  'created_date')
