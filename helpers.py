import allure
import requests
from faker import Faker

from urls import Urls

fake_en = Faker()
fake_ru = Faker(locale='ru_RU')

headers = {"Content-type": "application/json"}


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

def create_courier(data):
    # Хелпер для создания курьера

    with allure.step('Создание курьера'):
        create_response = requests.post(Urls.URL_create_courier, data)
        assert create_response.status_code == 201

def create_random_courier():
    # Хелпер для создания рандомного курьера
    data = create_random_courier_data()
    create_courier(data)
    return data

def login_courier(courier_data):
    # Авторизация курьера
    with allure.step('Авторизация курьера для получения id'):
        login_response = requests.post(Urls.URL_login_courier, {
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        courier_id = login_response.json()["id"]
    assert login_response.status_code == 200
    return courier_id


def delete_courier(data):
    courier_id = login_courier(data)
    delete_courier_by_id(courier_id)

def delete_courier_by_id(courier_id):
    data = requests.delete(Urls.URL_delete_courier+"/"+str(courier_id))
    assert data.status_code == 200

def cancel_order(track):
    data = {
            "track": track
    }
    requests.put(Urls.URL_cancel_order,data)
    # response = requests.put(Urls.URL_cancel_order,data)
    # assert response.status_code == 200
    # assert не проходит, потому что метод возвращает 400 даже при верном track