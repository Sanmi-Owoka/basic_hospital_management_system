from django.urls import path
from .views import DoctorSignUpViews, OnboardPatientViews, GetAllDoctors

urlpatterns = [
    path("doctor/signup", DoctorSignUpViews.as_view(), name="register"),
    path("onboard/patient/", OnboardPatientViews.as_view(), name="onboard_patient"),
    path("doctors/list/", GetAllDoctors.as_view(), name="get_all_doctors"),
]
