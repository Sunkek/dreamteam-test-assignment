from rest_framework_json_api import serializers

from .models import User, Group

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['email', 'password']

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'