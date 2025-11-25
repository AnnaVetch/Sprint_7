import json
import pytest
import requests
from helpers import *
from urls import *

class TestCreateCourier:
    def test_create_courier(self):
        payload = create_random_courier_data()

        headers = {"Content-type": "application/json"}
        payload_string = json.dumps(payload)
        response = requests.post(Urls.URL_create_courier, data=payload_string, headers=headers)

        assert 201 == response.status_code
        assert response.json()["ok"] == True


    def test_create_identical_courier(self):
        def test_create_courier(self):
            payload = create_random_courier_data()

            headers = {"Content-type": "application/json"}
            payload_string = json.dumps(payload)
            response = requests.post(Urls.URL_create_courier, data=payload_string, headers=headers)

            assert 201 == response.status_code
            print(response.json())
            assert response.json()["ok"] == True

            response = requests.post(Urls.URL_create_courier, data=payload_string, headers=headers)
            assert 409 == response.status_code
            assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."


    @pytest.mark.parametrize("login, password, firstname", [
        (create_random_login(), "", create_random_firstname()),
        ("", create_random_password(), create_random_firstname()),
    ])
    def test_create_courier_missing_field(self, login, password, firstname):
        data = {"login": login, "password": password, "firstName": firstname}
        response = requests.post(Urls.URL_create_courier, json=data)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"