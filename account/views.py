from django.shortcuts import render
from django.contrib.auth.views import LoginView

from account.accoun_services import checking_registration_data
from account.forms import AccountAuthenticationForm, UserRegistrationForm


class AccountLoginView(LoginView):
    """Redefinition AccountLoginView to use the form AccountAuthenticationForm"""
    form_class = AccountAuthenticationForm


def register(request):
    """Registration new User"""
    user_form = UserRegistrationForm()
    if request.method == 'POST':
        new_user = checking_registration_data(request.POST)
        if new_user:
            render(request,
                   'registration/register_done.html',
                   {'new_user': new_user})
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})
