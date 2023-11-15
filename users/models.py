import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("doctor", "doctor"),
        ("patient", "patient")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, null=True, max_length=50)
    temp_password = models.CharField(max_length=20, null=True)


class Appointment(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_appointment")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_appointment")
    appointment_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
