from rest_framework.test import APITestCase, APIClient
from django.urls import reverse, resolve
import pytest

pytestmark = pytest.mark.django_db


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = "doctor/signup/"
        self.login_url = "/api/v1/users/login/"
        self.change_password_url = "/api/v1/users/change_password/"
        self.update_profile_url = "/api/v1/users/update_profile/"

        self.register_data = {
            "first_name": "test",
            "last_name": "testing",
            "username": "testing@test.com",
            "password": "testingapi123"
        }

        self.login_data = {
            "username": "test",
            "password": "testingapi123"
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
