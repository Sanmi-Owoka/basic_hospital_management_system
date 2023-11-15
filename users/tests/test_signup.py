from .test_setup import *


class TestDoctorSignup(TestSetUp):
    def test_signup_correctly(self):
        client = APIClient()
        response = client.post(self.register_url, self.register_data, format='json')
        # print(response.txt)
        assert response.status_code == 201

    def test_signup_without_data(self):
        registration_data = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "password": ""
        }
        client = APIClient()
        response = self.client.post(self.register_url, self.register_data, format='json')
        print(response.json(), response.status_code)
        assert response.status_code == 400
