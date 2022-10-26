import requests
from typing import Any


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str) -> requests.Response:
        return requests.get(f"http://{self.base_url}{endpoint}")

    def post(self, endpoint: str, body: Any) -> requests.Response:
        return requests.post(f"http://{self.base_url}{endpoint}", data=body)

    def put(self, endpoint: str, body: Any) -> requests.Response:
        return requests.put(f"http://{self.base_url}{endpoint}", data=body)

    def delete(self, endpoint: str) -> requests.Response:
        return requests.delete(f"http://{self.base_url}{endpoint}")
