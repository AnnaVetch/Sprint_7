import allure
import requests

from urls import Urls

@allure.feature("Страница получение списка заказов")
class TestOrderList:
    @allure.title("Тест- получение списка заказов")
    def test_get_order_list(self):
        response = requests.get(Urls().URL_list_orders())

        assert 200 == response.status_code
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)