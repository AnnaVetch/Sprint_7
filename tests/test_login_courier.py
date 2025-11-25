import json

import pytest

import helpers
from helpers import *
from urls import Urls


@allure.feature("Страница авторизации курьера")
class TestCourierLogin:

    @allure.title("Тест- курьер может авторизоваться, успешный запрос возвращает id")
    def test_login_success(self):
        data = create_random_courier()

        data={
                'login': data['login'],
                'password': data['password']}
        with allure.step('Авторизация курьера для получения id'):
            login_response = requests.post(Urls.URL_login_courier, json.dumps(data), headers=headers)

            assert login_response.status_code == 200
            assert login_response.json()["id"] >0

        delete_courier(data)

    @pytest.mark.parametrize("login, password", [
        (helpers.create_random_login(), ""),
        ("", helpers.create_random_password()),
        ("",""),
    ])
    @allure.title("Тест-попытка авторизации с пропуском одного из обязательных полей")
    def test_login_missing_field(self, login, password):
        data = {"login": login, "password": password}
        response = requests.post(Urls.URL_login_courier, json.dumps(data), headers=headers)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Тест- авторизация курьера с неправильным логином")
    def test_login_wrong_login(self):
        data = create_random_courier_data()
        data.update({"login": "wrong"})

        response = requests.post(Urls.URL_login_courier, json.dumps(data), headers=headers)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Тест- авторизация курьера с неправильным паролем")
    def test_login_wrong_password(self):
        data = create_random_courier_data()
        data.update({"password": "wrong"})

        response = requests.post(Urls.URL_login_courier, json.dumps(data), headers=headers)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Тест- авторизация под несуществующим пользователем")
    def test_login_nonexistent_user(self):
        data = {
            "login": "user_does_not_exist_123",
            "password": "wrong_password_123"
        }

        response = requests.post(Urls.URL_login_courier, json.dumps(data), headers=headers)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"