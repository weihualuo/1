
from rest_framework import serializers
from users.models import *

# Normal serializer

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='user.username')
    email = serializers.Field(source='user.email')
    class Meta:
        model = Profile
        fields = ('id', 'name', 'email', 'image', 'status', 'gender', 'desc')

class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'image', 'status', 'gender', 'desc', 'user')

class ReverseProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'image', 'status', 'gender', 'desc')

class UserSerializer(serializers.ModelSerializer):
    profile = ReverseProfileSerializer(read_only=True, source='profile')
    class Meta:
        model = EndUser
        fields = ('id', 'username', 'email', 'first_name','profile')


class SimpleProfileSerialier(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('image',)

class SimpleUserSerializer(serializers.ModelSerializer):

    profile = SimpleProfileSerialier(read_only=True, source="profile")
    class Meta:
        model = EndUser
        fields = ('id', 'first_name', 'username', 'profile')