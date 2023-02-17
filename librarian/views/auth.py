from django.contrib.auth import views as auth_views
from librarian import forms


class LoginView(auth_views.LoginView):
    def __init__(self, arg):
        super(LoginView, self).__init__()
        self.authentication_form = forms.AuthenticationForm
