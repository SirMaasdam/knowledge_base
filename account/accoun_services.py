from account.forms import UserRegistrationForm
from account.tasks import user_created


def checking_registration_data(request_post):
    """Validation of registration data and user registration"""
    user_form = UserRegistrationForm(request_post)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(
            user_form.cleaned_data['password1'])
        new_user.save()
        # sending an email about successful registration
        user_created.delay(user_form.cleaned_data['username'], user_form.cleaned_data['email'])
        return new_user
