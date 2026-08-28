from rest_framework import serializers
from . models import Destinations, DestinationImages, Profile
from django.contrib.auth.models import User

class DestinationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destinations
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImages
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'