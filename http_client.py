import allure
import requests

from helpers import *

from urls import Urls

def create_courier(data):
    # Создания курьера с параметрами

    with allure.step('Создание курьера'):
        response = requests.post(Urls.URL_create_courier, data)
        assert response.status_code == 201
        assert response.json()["ok"] == True

def create_random_courier():
    # Создание рандомного курьера
    data = create_random_courier_data()
    create_courier(data)
    return data

def login_courier(courier_data):
    # Авторизация курьера
    with allure.step('Авторизация курьера для получения id'):
        response = requests.post(Urls.URL_login_courier, {
            'login': courier_data['login'],
            'password': courier_data['password']
        })
        courier_id = response.json()["id"]
    assert response.status_code == 200
    return courier_id

def delete_courier_by_id(courier_id):
    # Удаление курьера по идентификатору
    data = requests.delete(Urls.URL_delete_courier+"/"+str(courier_id))
    assert data.status_code == 200

def crate_order(courier_id):
    response = requests.post(Urls.URL_create_orders, json.dumps(data), headers=headers)
    track = response.json()["track"]

    assert response.status_code == 201
    assert track > 0