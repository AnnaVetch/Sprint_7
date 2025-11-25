import pytest
import requests

from data import TestOrder
from urls import Urls


class TestOrderCreate:


    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, color):
        payload = TestOrder().ORDER_DATA.copy()
        payload["color"] = color

        response = requests.post(Urls.URL_create_orders, json=payload)

        assert response.status_code == 201
        assert "track" in response.json()