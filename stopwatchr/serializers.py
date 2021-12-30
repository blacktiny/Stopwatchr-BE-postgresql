from rest_framework import serializers 
from stopwatchr.models import alerts, stocks, users
 
 
class UsersSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = users
        fields = (
            'id',
            'username',
            'useremail',
            'password',
            'alert_options',
        )

class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = stocks
        fields = (
            'id',
            'stockId',
            'user',
            'type',
            'name',
            'entry',
            'stop',
            'last_updated'
        )

class AlertsSerializer(serializers.ModelSerializer):
    stock = StocksSerializer(
        many=False,
        read_only=True
    )
    user = UsersSerializer(
        many=False,
        read_only=True
    )
    class Meta:
        model = alerts
        fields = (
            'id',
            'stock',
            'user',
            'created',
            'is_archived',
        )
