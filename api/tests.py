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
        assert response.status_code == 200
        assert response.data["error"] is True

    def test_api_response_error(self):
        request = self.factory.get(self.url, {"query": "MisyJA"})
        response = calculus(request)
        assert response.status_code == 200
        assert response.data["error"] is True
        assert response.data["message"] == "Contains prohibited operators"

    def test_api_response_success(self):
        request = self.factory.get(self.url, {"query": "Misy"})
        response = calculus(request)
        assert response.status_code == 200
        assert response.data["error"] is False
        assert response.data["result"] == "2+2"
