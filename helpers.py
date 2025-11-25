import allure
import requests
from faker import Faker

from urls import Urls

fake_en = Faker()
fake_ru = Faker(locale='ru_RU')


def create_random_login():
    login = fake_en.text(max_nb_chars=7) + str(fake_en.random_int(0, 999)) 
    return login


def create_random_password():
    password = fake_en.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    return password


def create_random_firstname():
    first_name = fake_ru.first_name()
    return first_name


def create_random_courier_data():
# Создает полный набор случайных данных для курьера
    return {
        'login': create_random_login(),
        'password': create_random_password(),
        'firstName': create_random_firstname()
    }

def create_random_courier():
    # Хелпер для создания курьера
    courier_data = {
        'login': create_random_login(),
        'password': create_random_password(),
        'firstName':create_random_firstname()
    }

    with allure.step('Создание курьера'):
        create_response = requests.post(Urls.URL_create_courier, data=courier_data)
        assert create_response.status_code == 201

    return courier_data

def login_courier():
    # Авторизация курьера
    courier_data = create_random_courier()

    with allure.step('Авторизация курьера для получения id'):
        login_response = requests.post(Urls.URL_login_courier, data={
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        courier_id = login_response.json()["id"]

    return {
        'data': courier_data,
        'id': courier_id
    }

def delete_courier(courier_id):
    courier_data = requests.delete(Urls.URL_delete_courier+"/"+str(courier_id))
    assert courier_data.status_code == 200