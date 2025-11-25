import json

import pytest

from data import TestOrder
from helpers import *


@allure.feature("Страница создание заказа самоката")
class TestOrderCreate:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title("Тест- при создании заказа можно выбрать разные вариации цвета самоката")
    def test_create_order_with_different_colors(self, color):
        data = TestOrder().ORDER_DATA.copy()
        data["color"] = color

        response = requests.post(Urls.URL_create_orders, json.dumps(data), headers=headers)
        track = response.json()["track"]

        assert response.status_code == 201
        assert track > 0
        
        cancel_order(track)