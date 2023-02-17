from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return u"%s %s" % (self.first_name, self.last_name)


class BookQuerySet(models.QuerySet):

    def available_for_user(self, user):
        return self.exclude(
            isbn__in=LoanLineItem.objects.filter(loan__user=user)
            .exclude(loan__status=Loan.RETURNED)
            .values("book")
        )
    
    def get_by_isbn(self, isbn):
        q = self.filter(isbn=isbn)
        return q.exists() and q.get()

class Book(models.Model):
    BOOK_OUT_OF_STOCK = 1
    BOOK_AVAILABLE = 0
    BOOK_ALREADY_LENT = 2

    isbn = models.BigIntegerField(primary_key=True, editable=True)
    title = models.CharField(max_length=500, db_index=True)
    authors = models.ManyToManyField(Author, related_name="books")
    description = models.TextField(blank=True)
    library = BookQuerySet.as_manager()

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title

    def in_stock(self):
        return self.stock.in_stock()

    def available_quantity(self):
        return self.stock.quantity

    def is_lent_to_user(self, user):
        return Loan.objects.is_book_lent_to_user(self, user)

    def is_in_user_basket(self, user):
        return Loan.objects.is_book_in_user_basket(self, user)

    def can_be_lent_to_user(self, user):
        lent = Loan.objects.is_book_lent_to_user(self, user)
        return self.in_stock() and not lent and not self.is_in_user_basket(user)

class StockQuerySet(models.QuerySet):
    def in_stock(self, book, quantity=1):
        q = self.filter(item=book)
        return q.exists() and q.get().quantity >= quantity

    def get_book_stock(self, book):
        q = self.filter(item=book)
        return q.exists() and q.get()

    def reserve(self, book, quantity):
        stock = self.filter(item=book).select_for_update().get()
        stock.reserve(quantity)

    def cancel_reservation(self, book, quantity):
        stock = self.filter(item=book).select_for_update().get()
        stock.cancel_reservation(quantity)

    def remove_item(self, book, quantity):
        stock = self.filter(item=book).select_for_update().get()
        stock.remove_item(quantity)

class Stock(models.Model):
    item = models.OneToOneField(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    records = StockQuerySet.as_manager()

    def reserve(self, quantity):
        if self.quantity < quantity:
            raise OutOfStockException("{} no está disponible".format(self.item))
        self.quantity = F("quantity") - quantity
        self.save()

    def cancel_reservation(self, quantity):
        self.quantity = F("quantity") + quantity
        self.save()

    def in_stock(self, quantity=1):
        return self.quantity >= quantity
    
    def remove_item(self, quantity):
        self.quantity = F("quantity") + quantity
        self.save()

class OutOfStockException(Exception):
    pass


class LoanQuerySet(models.QuerySet):
    def is_book_lent_to_user(self, book, user):
        return (
            self.filter(user=user, items__book=book)
            .exclude(status__in=[Loan.RETURNED, Loan.BASKET])
            .exists()
        )

    def is_book_in_user_basket(self, book, user):
        return self.filter(user=user, items__book=book, status=Loan.BASKET).exists()

    def active_basket(self, user):
        q = self.filter(user=user, status=Loan.BASKET)
        return q.exists() and q.get()
    
    def get_books_to_reserve(self, user):
        return self.filter(user=user, status=Loan.PLACED).values_list("items__book", flat=True)
    
    def get_dates_to_reserve(self, user):
        return self.filter(user=user, status=Loan.READY)

class Loan(models.Model):
    BASKET = "basket"
    PLACED = "placed"
    READY = "ready"
    LENT = "lent"
    RETURNED = "returned"
    STATUS_CHOICES = (
        (BASKET, "En progreso"),
        (PLACED, "Enviada"),
        (READY, "Lista para retirar"),
        (LENT, "Retirada"),
        (RETURNED, "Devuelta"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default=BASKET, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    max_return_date = models.DateTimeField(null=True)
    objects = LoanQuerySet.as_manager()

    def calculate_return_date(self):
        self.max_return_date = timezone.now() + timedelta(days=30)

    def place_reservation(self):
        self.status = Loan.PLACED

    def ready_for_pickup(self):
        self.status = Loan.READY
        self.calculate_return_date()
        self.save()

    def cancel(self):
        for item in self.items.all():
            item.cancel()
        self.delete()

class LoanLineItemQuerySet(models.QuerySet):
    def get_books_by_reference(self, reference):
        return self.filter(loan__reference=reference)
    
class LoanLineItem(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def cancel(self):
        Stock.records.cancel_reservation(book=self.book, quantity=self.quantity)
        self.delete()

    def get_all(self):
        return self.objects.all()