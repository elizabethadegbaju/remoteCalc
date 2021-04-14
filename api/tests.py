from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from .views import calculus


class ApiTestCase(APITestCase):
    def setUp(self):
        """
        Set up test fixtures
        """
        self.url = reverse('calculus')
        self.factory = APIRequestFactory()

    def test_bad_query(self):
        request = self.factory.get(self.url,
                                   {"query": "this is meant to fail"})
        response = calculus(request)
        assert response.status_code == 400
        assert response.data["error"] is True

    def test_api_response_error(self):
        request = self.factory.get(self.url, {"query": "MisyJA"})
        response = calculus(request)
        assert response.status_code == 400
        assert response.data["error"] is True
        assert response.data["message"] == "Contains prohibited operators"

    def test_api_response_success(self):
        request = self.factory.get(self.url, {
            "query": "MiAqICgyMy8oMzMpKS0gMjMgKiAoMjMp"})
        response = calculus(request)
        assert response.status_code == 200
        assert response.data["error"] is False
        assert int(response.data["result"]) == -527

    def test_api_response_deeply_nested(self):
        request = self.factory.get(self.url, {
            "query": "MiAqICgyMy8oMzMrNTAtMTAwKDYwKjIpKSktIDIzICogKDIzKQ"})
        response = calculus(request)
        assert response.status_code == 200
        assert response.data["error"] is False
        assert int(response.data["result"]) == -528
        
    def test_api_single_value_special_conditions(self):
        request = self.factory.get(self.url, {
            "query": "KCgoKC0xMCkpKSk="})
        response = calculus(request)
        assert response.status_code == 200
        assert response.data["error"] is False
        assert int(response.data["result"]) == -10
