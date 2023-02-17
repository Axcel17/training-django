from django.contrib import admin
from librarian.models import Book, Author, Loan


class BookAdmin(admin.ModelAdmin):
    print("hola, soy el admin de Book")
    pass


admin.site.register(Book, BookAdmin)


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorAdmin)


class LoanAdmin(admin.ModelAdmin):
    pass


admin.site.register(Loan, LoanAdmin)
