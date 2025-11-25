import json
import pytest
from helpers import *

@allure.feature("Страница создание курьера")
class TestCreateCourier:

    @allure.title("Тест- создание курьера")
    def test_create_courier(self):
        payload = create_random_courier_data()

        headers = {"Content-type": "application/json"}
        payload_string = json.dumps(payload)
        response = requests.post(Urls.URL_create_courier, data=payload_string, headers=headers)

        assert 201 == response.status_code
        assert response.json()["ok"] == True

    @allure.title("Тест- создание двух одинаковых курьеров")
    def test_create_identical_courier_error(self):
        payload = create_random_courier_data()

        headers = {"Content-type": "application/json"}
        payload_string = json.dumps(payload)
        response1 = requests.post(Urls.URL_create_courier, data=payload_string, headers=headers)

        assert 201 == response1.status_code
        assert response1.json()["ok"] == True

        response2 = requests.post(Urls.URL_create_courier, data=payload_string, headers=headers)
        assert 409 == response2.status_code
        assert response2.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize("login, password, firstname", [
        (create_random_login(), "", create_random_firstname()),
        ("", create_random_password(), create_random_firstname()),
    ])
    @allure.title("Тест- создание курьера, если одного из обязательных полей нет")
    def test_create_courier_missing_field(self, login, password, firstname):
        data = {"login": login, "password": password, "firstName": firstname}
        response = requests.post(Urls.URL_create_courier, json=data)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
