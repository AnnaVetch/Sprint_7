import pytest
from courier_helpers import *
class TestCourierLogin:


    def test_login_success(self):
        courier_data = {
            'login': helpers.create_random_login(),
            'password': helpers.create_random_password(),
            'firstName': helpers.create_random_firstname()
        }

        with allure.step('Создание курьера'):
            create_response = requests.post(Urls.URL_create_courier, data=courier_data)
            assert create_response.status_code == 201

        with allure.step('Авторизация курьера для получения id'):
            login_response = requests.post(Urls.URL_login_courier, data={
                'login': courier_data['login'],
                'password': courier_data['password']
            })

            assert login_response.status_code == 200
            assert login_response.json()["id"] >0


    @pytest.mark.parametrize("login, password", [
        (helpers.create_random_login(), ""), ("", helpers.create_random_password()),
    ])
    def test_login_missing_field(self, login, password):
        data = {"login": login, "password": password}
        response = requests.post(Urls.URL_login_courier, json=data)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"


    def test_login_wrong_login(self):
        courier_data = create_random_courier()
        courier_data.update({"login": "wrong"})

        response = requests.post(Urls.URL_login_courier, json=courier_data)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    def test_login_wrong_password(self):
        courier_data = create_random_courier()
        courier_data.update({"password": "wrong"})

        response = requests.post(Urls.URL_login_courier, json=courier_data)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @pytest.mark.parametrize("data", [
        {"password": helpers.create_random_password()},
        {"login": helpers.create_random_login()},
        {},
    ])
    def test_login_missing_field(self, data):
        response = requests.post(Urls.URL_login_courier, json=data)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"


    def test_login_nonexistent_user(self):
        data = {
            "login": "user_does_not_exist_123",
            "password": "wrong_password_123"
        }

        response = requests.post(Urls.URL_login_courier, json=data)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"