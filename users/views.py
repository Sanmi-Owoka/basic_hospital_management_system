from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import SignUpSerializer, OnboardPatientSerializer, GetDoctorsSerializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


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
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                username=serializer.validated_data["username"],
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
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                username=serializer.validated_data["username"],
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


class BookAppointmentViews(generics.GenericAPIView):
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def post(self, request):
        patient = request.user
        serializer = self.serializer_class(request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "message": "failure",
                    "data": "null",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


