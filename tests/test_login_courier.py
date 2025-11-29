import json

import allure
import pytest

import helpers


@allure.feature("Страница авторизации курьера")
class TestCourierLogin:

    @allure.title("Тест- курьер может авторизоваться, успешный запрос возвращает id")
    def test_login_success(self, make_courier):
        # Arrange
        data, client = make_courier

        # Act
        data = {
            'login': data['login'],
            'password': data['password']}
        with allure.step('Авторизация курьера для получения id'):
            login_response = client.login_courier(json.dumps(data))

            # Assert
            assert login_response.status_code == 200
            assert login_response.json()["id"] > 0

    @pytest.mark.parametrize("login, password", [
        (helpers.create_random_login(), ""),
        ("", helpers.create_random_password()),
        ("", ""),
    ])
    @allure.title("Тест-попытка авторизации с пропуском одного из обязательных полей")
    def test_login_missing_field(self, make_courier, login, password):
        _, client = make_courier
        data = {"login": login, "password": password}
        response = client.login_courier(json.dumps(data))

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Тест- авторизация курьера с неправильным логином")
    def test_login_wrong_login(self, make_courier):
        data, client = make_courier
        wrong_data = data.copy()
        wrong_data.update({"login": "wrong"})

        response = client.login_courier(json.dumps(wrong_data))

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Тест- авторизация курьера с неправильным паролем")
    def test_login_wrong_password(self, make_courier):
        data, client = make_courier
        wrong_data=data.copy()
        wrong_data.update({"password": "wrong"})

        response = client.login_courier(json.dumps(wrong_data))

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Тест- авторизация под несуществующим пользователем")
    def test_login_nonexistent_user(self, make_courier):
        _, client = make_courier
        data = {
            "login": "user_does_not_exist_123",
            "password": "wrong_password_123"
        }

        response = client.login_courier(json.dumps(data))

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
