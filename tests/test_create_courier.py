import json

import pytest
from helpers import *

@allure.feature("Страница создание курьера")
class TestCreateCourier:

    @allure.title("Тест- создание курьера")
    def test_create_courier(self):
        data = create_random_courier_data()

        response = requests.post(Urls.URL_create_courier, json.dumps(data), headers=headers)

        print(response.content.decode('utf-8'))
        assert response.status_code == 201
        assert response.json()["ok"] == True

        delete_courier(data)

    @allure.title("Тест- создание двух одинаковых курьеров")
    def test_create_identical_courier_error(self):
        data = create_random_courier_data()

        response1 = requests.post(Urls.URL_create_courier, json.dumps(data), headers=headers)

        assert response1.status_code == 201
        assert response1.json()["ok"] == True

        response2 = requests.post(Urls.URL_create_courier, json.dumps(data), headers=headers)
        assert response2.status_code == 409
        assert response2.json()["message"] == "Этот логин уже используется. Попробуйте другой."

        delete_courier(data)

    @pytest.mark.parametrize("login, password, firstname", [
        (create_random_login(), "", create_random_firstname()),
        ("", create_random_password(), create_random_firstname()),
    ])
    @allure.title("Тест- создание курьера, если одного из обязательных полей нет")
    def test_create_courier_missing_field(self, login, password, firstname):
        data = {"login": login, "password": password, "firstName": firstname}
        response = requests.post(Urls.URL_create_courier, json.dumps(data), headers=headers)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
