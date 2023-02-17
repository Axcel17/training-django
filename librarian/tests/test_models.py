from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from librarian.models import Book, Loan
from librarian.api import BookLoan


class BookLoanOnlyOneBasketTest(TestCase):
    fixtures = [
        "users",
        "authors",
        "books",
        "stock",
        "test_one_basket",
    ]

    def setUp(self):
        pass

    def test_only_one_loan_with_basket_status_should_exist(self):
        """
        complete the test
        """
        pass

    def test_is_lent_to_user_juanita(self):
        """
        complete the test
        """
        pass

    def test_book_can_be_lent_to_user_juanita(self):
        """
        Hint: the book The Odyssey can be lent

        complete the test
        """
        pass

    def test_book_cannot_be_lent_to_user_juanita(self):
        """
        Hint: the book One Hundred Years of Solitude canno be lent

        complete the test
        """
        pass
