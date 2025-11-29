import json

import allure
import pytest
from helpers import *

@allure.feature("Страница создание курьера")
class TestCreateCourier:

    @allure.title("Тест- создание курьера")
    def test_create_courier(self,courier_cleanup_context):
        # Arrange
        ctx,client = courier_cleanup_context
        ctx["data"] = create_random_courier_data()

        # Act
        response = client.create_courier(json.dumps(ctx["data"]))
        # Assert
        assert response.status_code == 201
        assert response.json()["ok"] == True


    @allure.title("Тест- создание двух одинаковых курьеров")
    def test_create_identical_courier_error(self,courier_cleanup_context):
        # Arrange
        ctx,client = courier_cleanup_context
        ctx["data"] = create_random_courier_data()
        response1 = client.create_courier(json.dumps(ctx["data"]))

        # Act
        response2 = client.create_courier(json.dumps(ctx["data"]))

        # Assert
        assert response1.status_code == 201
        assert response2.status_code == 409
        assert response2.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize("login, password, firstname", [
        (create_random_login(), "", create_random_firstname()),
        ("", create_random_password(), create_random_firstname()),
    ])
    @allure.title("Тест- создание курьера, если одного из обязательных полей нет")
    def test_create_courier_missing_field(self, make_http_client, login, password, firstname):
        # Arrange
        client=make_http_client
        data = {"login": login, "password": password, "firstName": firstname}

        # Act
        response = client.create_courier(json.dumps(data))

        # Assert
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"