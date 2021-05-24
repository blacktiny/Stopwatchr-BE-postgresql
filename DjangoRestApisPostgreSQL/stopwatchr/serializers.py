from rest_framework import serializers 
from stopwatchr.models import users
 
 
class UsersSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = users
        fields = ('id',
                  'username',
                  'useremail',
                  'password')
