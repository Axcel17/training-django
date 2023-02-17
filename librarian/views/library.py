from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User

from librarian.models import Book, Loan, LoanLineItem
from librarian.api import BookLoan


@login_required()
@require_http_methods(["GET"])
def index(request):

    data = {
        "library": [
            {
                "isbn": book.isbn,
                "title": book.title,
                "description": book.description,
                "authors": book.authors.all()[0],
                "can_be_lent_to_user": book.can_be_lent_to_user(request.user),
                "available_quantity": book.available_quantity(),
                "is_lent_to_user": book.is_lent_to_user(request.user),
                "is_in_user_basket": book.is_in_user_basket(request.user),
            }
            for book in Book.library.all()
        ],
        "basket": Loan.objects.active_basket(request.user),
        "is_staff": User.objects.get(username=request.user).is_staff,
    }

    return render(request, "library/app.html", data)

@login_required()
@require_http_methods(["GET"])
def myloans(request):
    
    data = {
        "library": [
            {
                "title": LoanLineItem.objects.get(loan=reference).book.title,
                "authors": LoanLineItem.objects.get(loan=reference).book.authors.all()[0],
                "isbn": LoanLineItem.objects.get(loan=reference).book.isbn,
                "description": LoanLineItem.objects.get(loan=reference).book.description,
                "created_at": reference.created_at.strftime("%d/%m/%Y:%H - %M:%S"),
                "max_return_date": reference.max_return_date.strftime("%d/%m/%Y - %H:%M:%S"),
                "status": reference.status,
            }
            for reference in Loan.objects.get_dates_to_reserve(request.user)
        ],
    }

    return render(request, "loans/loans.html", data)

@login_required()
@require_http_methods(["POST"])
def add_to_basket(request, isbn):
    loan = BookLoan(request.user)
    book = Book.library.get_by_isbn(isbn)
    loan.add_book(book)
    return redirect("home")


@login_required()
@require_http_methods(["POST"])
def remove_from_basket(request, isbn):
    loan = BookLoan(request.user)
    book = Book.library.get_by_isbn(isbn)
    loan.remove_book(book)
    return redirect("home")

@login_required()
@require_http_methods(["POST"])
def place_reservation(request):

    loan = BookLoan(request.user)
    loan.place_reservation()

    return redirect("checkout-complete")

@login_required()
@require_http_methods(["POST"])
def pick_reserved_books(request):
    loan = BookLoan(request.user)
    loan.ready_for_pickup()
    return redirect("home")

@login_required()
@require_http_methods(["POST"])
def cancel_reservation(request):
    loan = BookLoan(request.user)
    loan.cancel()
    return redirect("home")

@login_required()
@require_http_methods(["GET"])
def checkout_complete(request):
    isbn_book = list(BookLoan(request.user)._init_items().keys())[0]
    # isbn_books = list(Loan.objects.get_books_to_reserve(request.user))
    data = {
        "books_to_reserve": [
            {
                "isbn": book.isbn,
                "title": book.title,
                "description": book.description,
                "authors": book.authors.all()[0],
            }
            for book in Book.library.all() if book.isbn == isbn_book
        ],
    }
    
    return render(request, "checkout/complete.html", data)


