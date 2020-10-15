import requests
import json
import random


def group_create():
    for i in range(1, 10):
        params = {
            "title": f"group {i}"
        }

        resp = requests.post('http://127.0.0.1:8000/group', data=json.dumps(params))

        if resp.ok:
            print(resp.json())


def product_create():
    for i in range(1, 150):
        params = {
            "title": f"product {i}",
            "sku": f"P0000{i}",
            "remain": random.randint(5, 50),
            "group_id": random.randint(1, 10)
        }

        resp = requests.post('http://127.0.0.1:8000/product', data=json.dumps(params))

        if resp.ok:
            print(resp.json())


group_create()
product_create()
