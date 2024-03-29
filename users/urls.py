from django.urls import path
from .views import (
    DoctorSignUpViews,
    OnboardPatientViews,
    GetAllDoctors,
    LoginView,
    BookAppointmentViews,
    GetAppointmentView,
    GetProfileView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("doctor/signup/", DoctorSignUpViews.as_view(), name="register"),
    path("onboard/patient/", OnboardPatientViews.as_view(), name="onboard_patient"),
    path("doctors/list/", GetAllDoctors.as_view(), name="get_all_doctors"),
    path("book/appointment/", BookAppointmentViews.as_view(), name="book_appointment"),
    path("appointment/list/", GetAppointmentView.as_view(), name="get_appointments"),
    path("profile/", GetProfileView.as_view(), name="get_profile")
]
