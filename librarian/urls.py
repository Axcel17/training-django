from django.urls import path
from django.contrib.auth import views as auth_views
from librarian import forms
from librarian.views import library

urlpatterns = [
    path("", library.index, name="home"),
    path("myloans/", library.myloans, name="myloans"),
    path("add-to-basket/<int:isbn>", library.add_to_basket, name="add-to-basket"),
    path(
        "remove-from-basket/<int:isbn>",
        library.remove_from_basket,
        name="remove-from-basket",
    ),
    path(
        "place-reservation",
        library.place_reservation,
        name="place-reservation",
    ),
    path(
        "checkout-complete",
        library.checkout_complete,
        name="checkout-complete",
    ),
    path(
        "pick-reserved-books",
        library.pick_reserved_books,
        name="pick-reserved-books",
    ),
    path("cancel-reservation", library.cancel_reservation, name="cancel-reservation"),

    path(
        "signin/",
        auth_views.LoginView.as_view(authentication_form=forms.AuthenticationForm),
    ),
]
