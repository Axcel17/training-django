from librarian.models import Loan, LoanLineItem, Stock
from django.db import transaction
from django.utils import timezone
from datetime import timedelta


class BookLoan(object):
    PREVIOUSLY_LOANED_ERROR_MSG = (
        "Ya tienes este título. Debes devolverlo antes de pedirlo nuevamente."
    )
    ONE_TITLE_PER_LOAN = "Solo puedes prestar un ejemplar de un título a la vez."
    OUT_OF_STOCK = 1
    BOOK_AVAILABLE = 0
    BOOK_ALREADY_LENT = 2

    def __init__(self, user):
        super(BookLoan, self).__init__()
        self.user = user
        active_basket = Loan.objects.active_basket(user)
        self.loan = active_basket or Loan(user=user)
        self.books = self._init_items()
        
        self.loan.save()

    def add_book(self, book, quantity=1):
        if self.books.get(book.isbn):
            raise Exception(BookLoan.ONE_TITLE_PER_LOAN)
        if Loan.objects.is_book_lent_to_user(book, self.user):
            raise Exception(BookLoan.PREVIOUSLY_LOANED_ERROR_MSG)

        with transaction.atomic():
            line_item = LoanLineItem(loan=self.loan, quantity=quantity, book=book)
            Stock.records.reserve(book, quantity)
            self.books[book.isbn] = line_item

            line_item.save()

    def remove_book(self, book):
        with transaction.atomic():
            line_item = self.books.pop(book.isbn)
            Stock.records.remove_item(book, line_item.quantity)
            line_item.delete()

    def place_reservation(self):
        with transaction.atomic():
            self.loan.place_reservation()

    def ready_for_pickup(self):
        with transaction.atomic():
            self.loan.ready_for_pickup()

    def cancel(self):
        with transaction.atomic():
            self.loan.cancel()

    def is_book_available(self, book):
        lent = Loan.objects.is_book_lent_to_user(book, self.user)
        if book.in_stock() and not lent:
            return BookLoan.BOOK_AVAILABLE
        elif not book.in_stock():
            return BookLoan.BOOK_OUT_OF_STOCK
        elif lent:
            return BookLoan.BOOK_ALREADY_LENT
    
    def _init_items(self):
        return {item.book.isbn: item for item in self.loan.items.all()}