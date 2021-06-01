from django.db.models import fields
from rest_framework import serializers 
from stopwatchr.models import stocks, users
 
 
class UsersSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = users
        fields = (
            'id',
            'username',
            'useremail',
            'password',
        )

class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = stocks
        fields = (
            'stockId',
            'userId',
            'type',
            'name',
            'entry',
            'stop',
        )
