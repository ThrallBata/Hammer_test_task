from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):

    # token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Profile
        fields = ('phone', 'invite_code', 'token')

    # def create(self, validated_data):
    #     return Profile.objects.create_profile(**validated_data)
