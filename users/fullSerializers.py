from rest_framework import serializers

from favourites.serializers import FavouritesSerializer
from records.serializers import RecordSerializer
from users.models import User


class FullUserSerializer(serializers.ModelSerializer):
    records = RecordSerializer(many=True)
    favourites = FavouritesSerializer(many=True)

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
                  'created_date',
                  'records',
                  'favourites')
