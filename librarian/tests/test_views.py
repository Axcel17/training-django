from rest_framework import status
from django.test.testcases import TestCase, Client
from django.urls import reverse


class TestLibraryViews(TestCase):
    fixtures = ["users", "authors", "books", "stock", "loans"]

    def setUp(self):
        self.client = Client()
        self.client.login(username="juanita", password="12345678")

    def test_index_view_returns_status_200_GET(self):
        """
        complete the test
        """
        pass

    def test_index_view_returns_expected_parameters(self):
        """
        complete the test
        """
        pass

    def test_add_to_basket_view_redirect_to_home_view(self):
        """
        complete the test
        """
        pass
