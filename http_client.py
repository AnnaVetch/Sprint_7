import allure
import requests

from helpers import *


class HttpClient:
    def __init__(self, host):
        self.url_create_courier = f'{host}api/v1/courier/'
        self.url_login_courier = f'{host}api/v1/courier/login'
        self.url_delete_courier = f'{host}api/v1/courier'
        self.url_create_orders = f'{host}api/v1/orders'
        self.url_list_orders = f'{host}api/v1/orders'
        self.url_accept_orders = f'{host}api/v1/orders/accept'
        self.url_get_orders = f'{host}api/v1/orders/track'
        self.url_cancel_order = f'{host}api/v1/orders/cancel'

    def create_courier(self, data):
        # Создания курьера с параметрами
        with allure.step('Создание курьера'):
            response = requests.post(self.url_create_courier, data, headers=headers)
            return response

    def login_courier(self, data):
        # Авторизация курьера
        with allure.step('Авторизация курьера для получения id'):
            response = requests.post(self.url_login_courier, data, headers=headers)
            return response

    def delete_courier_by_id(self, courier_id):
        # Удаление курьера по идентификатору
        with allure.step('Удаление курьера'):
            response = requests.delete(self.url_delete_courier + "/" + str(courier_id))
        assert response

    def crate_order(self, data):
        # Создание заказа
        with allure.step('Создание заказа'):
            response = requests.post(self.url_create_orders, data, headers=headers)

        return response

    def get_list_orders(self):
        # Получение заказа
        with allure.step('Получение заказа'):
            response = requests.get(self.url_list_orders, headers=headers)

        return response

    def cancel_order(self, data):
        # Отмена заказа
        with allure.step('Отмена заказа'):
            response = requests.put(self.url_cancel_order, data)
        return response
