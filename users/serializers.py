from rest_framework import serializers
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=50, required=True, min_length=3)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password"
        ]
        write_only_fields = [
            "password"
        ]
        read_only_fields = [
            "date_joined"
        ]


class OnboardPatientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=50, required=True, min_length=3, write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password"
        ]
        read_only_fields = [
            "date_joined"
        ]


class GetDoctorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "date_joined",
        ]
        read_only_fields = [
            "first_name",
            "last_name",
            "username",
            "date_joined",
        ]
