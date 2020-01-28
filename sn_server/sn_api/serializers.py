from rest_framework_json_api import serializers

from .models import User, Group

class UserSerializer(serializers.ModelSerializer):
    """This class is used to manage how we pass User to the client app."""

    class Meta:
        model = User
        exclude = ['email', 'password']

class GroupSerializer(serializers.ModelSerializer):
    """This class is used to manage how we pass Group to the client app."""

    class Meta:
        model = Group
        fields = '__all__'