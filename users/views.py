from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import (
    SignUpSerializer,
    OnboardPatientSerializer,
    GetDoctorsSerializers,
    LoginSerializer,
    BookAppointmentSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from users.models import User, Appointment


class DoctorSignUpViews(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            new_user = User.objects.create(
                first_name=serializer.validated_data["first_name"].lower().strip(),
                last_name=serializer.validated_data["last_name"].lower().strip(),
                username=serializer.validated_data["username"].lower().strip(),
                user_type="doctor"
            )
            new_user.set_password(serializer.validated_data["password"])
            new_user.save()
            token = RefreshToken.for_user(new_user)
            return Response(
                {
                    "message": "success",
                    "data": {
                        "user": serializer.data,
                        "token": str(token.access_token)
                    },
                    "errors": "null"
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": F"{e}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class OnboardPatientViews(generics.GenericAPIView):
    serializer_class = OnboardPatientSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if not request.user.user_type == "doctor":
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": "user unauthorized for this action"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            data = request.data
            temp_password = request.data["password"]
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            new_user = User.objects.create(
                first_name=serializer.validated_data["first_name"].lower().strip(),
                last_name=serializer.validated_data["last_name"].lower().strip(),
                username=serializer.validated_data["username"].lower().strip(),
                user_type="patient",
                temp_password=temp_password
            )
            new_user.set_password(serializer.validated_data["password"])
            new_user.save()
            return Response(
                {
                    "message": "success",
                    "data": {
                        "user": serializer.data,
                        "password": temp_password
                    },
                    "errors": "null"
                },
                status=status.HTTP_201_CREATED
            )
        except TypeError as e:
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": f"{e} is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": f"{e}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class GetAllDoctors(generics.GenericAPIView):
    serializer_class = GetDoctorsSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if not request.user.user_type == "patient":
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": "user unauthorized for this action"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            all_doctors = User.objects.filter(user_type="doctor")
            response = self.serializer_class(all_doctors, many=True)
            return Response(
                {
                    "message": "success",
                    "data": response.data,
                    "errors": "null"
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": e
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            get_user = User.objects.filter(username=serializer.validated_data["username"])
            if not get_user.exists():
                username = serializer.validated_data["username"]
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"user with username: {username} does not exists"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = get_user.first()
            if not user.check_password(serializer.validated_data["password"]):
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"Invalid credentials"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken.for_user(user)
            response = self.serializer_class(user)
            return Response(
                {
                    "message": "success",
                    "data": {
                        "user": response.data,
                        "token": str(token.access_token)
                    },
                    "errors": "null"
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": f"{e}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class BookAppointmentViews(generics.GenericAPIView):
    serializer_class = BookAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            patient = request.user
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            doctor_username = serializer.validated_data["doctor_username"]
            appointment_time = serializer.validated_data["appointment_time"]
            get_doctor = User.objects.filter(username=doctor_username)

            if not get_doctor.exists():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"Doctor with username: {doctor_username} does not exists"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            get_doctor = get_doctor.first()
            if not get_doctor.user_type == "doctor":
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"Doctor with username: {doctor_username} does not exists"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            check_doctor_has_appointment = Appointment.objects.filter(
                doctor=get_doctor,
                appointment_time=appointment_time
            )

            if check_doctor_has_appointment.exists():
                return Response(
                    {
                        "message": "failure",
                        "data": "null",
                        "errors": f"Doctor already has an appointment at the slated time"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            new_appointment = Appointment.objects.create(
                doctor=get_doctor,
                patient=patient,
                appointment_time=appointment_time
            )
            response = self.serializer_class(new_appointment)
            return Response(
                {
                    "message": "success",
                    "data": {
                        "appointment": response.data,
                    },
                    "errors": "null"
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": f"{e}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class GetAppointmentView(generics.GenericAPIView):
    serializer_class = BookAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if user.user_type == "patient":
                get_appointment = Appointment.objects.filter(patient=user)
            else:
                get_appointment = Appointment.objects.filter(doctor=user)
            response = self.serializer_class(get_appointment, many=True)
            return Response(
                {
                    "message": "success",
                    "data": {
                        "appointment": response.data,
                    },
                    "errors": "null"
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": f"{e}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class GetProfileView(generics.GenericAPIView):
    serializer_class = GetDoctorsSerializers
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            response = self.serializer_class(user)
            return Response(
                {
                    "message": "success",
                    "data": response.data,
                    "errors": "null"
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": f"{e}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
