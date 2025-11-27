import allure


@allure.feature("Страница получение списка заказов")
class TestOrderList:
    @allure.title("Тест- получение списка заказов")
    def test_get_order_list(self, make_http_client):
        client = make_http_client
        response = client.get_list_orders()

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
