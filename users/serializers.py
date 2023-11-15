from rest_framework import serializers
from .models import User, Appointment


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


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=50, required=True, min_length=3, write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "date_joined",
            "password",
        ]

        read_only_fields = [
            "first_name",
            "last_name",
            "date_joined"
        ]


class BookAppointmentSerializer(serializers.ModelSerializer):
    doctor_username = serializers.CharField(max_length=150, required=True, write_only=True)
    appointment_time = serializers.DateTimeField()
    doctor = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "doctor",
            "patient",
            "appointment_time",
            "created_at",
            "updated_at",
            "doctor_username",
        ]

        read_only_fields = [
            "doctor",
            "patient",
            "created_at",
            "updated_at"
        ]

    def get_doctor(self, instance):
        try:
            doctor = instance.doctor
            return {
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
                "username": doctor.username
            }
        except:
            return None

    def get_patient(self, instance):
        try:
            patient = instance.patient
            return {
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "username": patient.username
            }
        except:
            return None
