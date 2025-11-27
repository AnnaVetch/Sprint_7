import json

import allure
import pytest

from data import TestOrder


@allure.feature("Страница создание заказа самоката")
class TestOrderCreate:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title("Тест- при создании заказа можно выбрать разные вариации цвета самоката")
    def test_create_order_with_different_colors(self, order_cleanup_context, color):
        # Arrange
        ctx, client = order_cleanup_context
        data = TestOrder().ORDER_DATA.copy()
        data["color"] = color

        # Act
        response = client.crate_order(json.dumps(data))
        ctx["data"] = response.content

        # Assert
        assert response.status_code == 201
        assert response.json()["track"] > 0
