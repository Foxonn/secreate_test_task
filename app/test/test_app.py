from fastapi.testclient import TestClient
import sys
import os

# remove test db
if os.path.isfile(os.path.join(os.path.curdir, 'sql_app.db')):
    os.remove(os.path.join(os.path.curdir, 'sql_app.db'))

sys.path.append("/app")
from app import app

client = TestClient(app)


def test_create_group():
    params = {
        'title': ' group 1 '
    }

    response = client.post("/group/", json=params)
    assert response.status_code == 200
    assert response.json() == {"title": "group 1", "id": 1}


def test_create_group_duplicate_title():
    params = {
        'title': ' group 1 '
    }

    response = client.post("/group/", json=params)
    assert response.status_code == 400


def test_get_group():
    response = client.get("/group/?id=1")
    assert response.status_code == 200
    assert response.json() == {"title": "group 1", "id": 1, "products": []}


def test_create_product_1():
    params = {
        "title": "milk",
        "sku": "220FFG",
        "remain": 20,
        "group_id": 1
    }
    response = client.post("/product/", json=params)
    assert response.status_code == 200
    assert response.json() == {"title": "milk", "sku": "220FFG", "remain": 20,
                               "id": 1, "reserved": 0, "group_id": 1}


def test_create_product_2():
    params = {
        "title": "cucumber",
        "sku": "220FFGY",
        "remain": 20,
        "group_id": 1
    }
    response = client.post("/product/", json=params)
    assert response.status_code == 200
    assert response.json() == {"title": "cucumber", "sku": "220FFGY",
                               "remain": 20,
                               "id": 2, "reserved": 0, "group_id": 1}


def test_create_product_not_exist_group():
    params = {
        "title": "milk",
        "sku": "220FFGN",
        "remain": 20,
        "group_id": 5
    }
    response = client.post("/product/", json=params)
    assert response.status_code == 400


def test_create_product_duplicate_sku():
    params = {
        "title": "milk",
        "sku": "220FFG",
        "remain": 20,
        "group_id": 1
    }
    response = client.post("/product/", json=params)
    assert response.status_code == 400


def test_get_product():
    response = client.get("/product/?id=1")
    assert response.status_code == 200
    assert response.json() == {"title": "milk", "sku": "220FFG", "remain": 20,
                               "id": 1, "reserved": 0, "group_id": 1}


def test_update_product():
    params = {
        "title": "MILK"
    }

    response = client.put("/product/?id=1", json=params)
    assert response.status_code == 200
    assert response.json() == {"title": "MILK", "sku": "220FFG", "remain": 20,
                               "id": 1, "reserved": 0, "group_id": 1}


def test_update_products():
    params = [{"id": 1, "title": "MILKK"}, {"id": 2, "title": "CuCumber"}]

    response = client.put("/products/", json=params)
    assert response.status_code == 200
    assert response.json() == [
        {"title": "MILKK", "sku": "220FFG", "remain": 20,
         "id": 1, "reserved": 0, "group_id": 1},
        {"title": "CuCumber", "sku": "220FFGY", "remain": 20,
         "id": 2, "reserved": 0, "group_id": 1}
    ]


def test_get_group_with_product():
    response = client.get("/group/?id=1")
    assert response.status_code == 200
    assert response.json() == {"title": "group 1", "id": 1, "products": [
        {"title": "MILKK", "sku": "220FFG", "remain": 20,
         "id": 1, "reserved": 0, "group_id": 1},
        {"title": "CuCumber", "sku": "220FFGY", "remain": 20,
         "id": 2, "reserved": 0, "group_id": 1}]}


def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == [
        {"title": "MILKK", "sku": "220FFG", "remain": 20,
         "id": 1, "reserved": 0, "group_id": 1},
        {"title": "CuCumber", "sku": "220FFGY", "remain": 20,
         "id": 2, "reserved": 0, "group_id": 1}]


def test_delete_product():
    response = client.delete("/product/?id=1")
    assert response.status_code == 200
    assert response.json() == "success"
