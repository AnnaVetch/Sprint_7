import json

import pytest

import helpers
import http_client


@pytest.fixture
def make_http_client():
    # Фикстура для создания HttpClient

    # setup
    client = http_client.HttpClient('https://qa-scooter.praktikum-services.ru/')
    return client


@pytest.fixture
def courier_cleanup_context(make_http_client):
    # Фикстура для очистки курьера

    # setup
    client = make_http_client
    ctx = {}
    yield ctx, client

    # teardown
    response = client.login_courier(json.dumps(ctx["data"]))
    courier_id = response.json()["id"]
    client.delete_courier_by_id(courier_id)


@pytest.fixture
def make_courier(make_http_client):
    # Фикстура для создания и очистки курьера

    # setup
    client = make_http_client
    data = helpers.create_random_courier_data()
    client.create_courier(json.dumps(data))
    yield data, client

    # teardown
    response = client.login_courier(json.dumps(data))
    courier_id = response.json()["id"]
    client.delete_courier_by_id(courier_id)


@pytest.fixture
def order_cleanup_context(make_http_client):
    # Фикстура для отмены заказа

    # setup
    client = make_http_client
    ctx = {}
    yield ctx, client

    # teardown
    client.cancel_order(ctx["data"])
