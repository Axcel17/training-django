from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from librarian.models import Book, Loan
from librarian.api import BookLoan


class BookLoanOneCopyAtATimeTest(TestCase):
    fixtures = [
        "users",
        "authors",
        "books",
        "stock",
        "test_one_copy_at_a_time",
    ]

    def setUp(self):
        pass

    def test_add_book_fails_when_adding_a_previously_added_book(self):
        """
        Hint: this book has been added to the cart by user juanita
        """
        user = User.objects.get(username="juanita")
        don_quixote = 9780142437230

        # Complete the test
        
        



    def test_add_book_fails_if_someone_attemps_to_add_an_unreturned_book(self):
        """
        Hint: this book has been lent by user juanita
        """
        user = User.objects.get(username="juanita")
        one_hundred_years_of_solitude = 60883286

        # Complete the test


class BookLoanReturnDateCalculationTest(TestCase):
    fixtures = ["users", "authors", "books", "stock"]

    def setUp(self):
        pass

    def test_max_return_date_is_30_days_after_placing_reservation(self):

        # Complete the test


        pass
