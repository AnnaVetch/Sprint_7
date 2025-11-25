class TestData:
    # Статические данные, существующая учетка
    correct_login = "Terik"
    correct_password = "1234"
    correct_first_name = "sobakin"
    valid_courier_fields = {"login": "Terik", "password": "1234", "firstName": "sobakin"}
    courier_without_firstname = {"login": "Terik", "password": "1234"}
    courier_wrong_password = {"login": "Terik", "password": "123456"}


class TestOrder:
    ORDER_DATA = {
        "firstName": "Михаил",
        "lastName": "Булгаков",
        "address": "Большая Садовая, 32",
        "metroStation": 8,
        "phone": "+79206709875",
        "rentTime": 2,
        "deliveryDate": "2025-12-07",
        "comment": "С попутным ветром!",
        "color": ["BLACK"]
    }