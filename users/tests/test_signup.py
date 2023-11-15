from .test_setup import *


class TestDoctorSignup(TestSetUp):
    def test_signup_correctly(self):
        client = APIClient()
        response = client.post(self.register_url, self.register_data)
        print(response.txt)
        assert response.status_code == 201

    def test_signup_without_data(self):
        registration_data = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "password": ""
        }
        client = APIClient()
        response = client.post(self.register_url, self.register_data)
        print(response.txt)
        assert response.status_code == 400