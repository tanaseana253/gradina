# myapp/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


class LogInForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class SignUpForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Parolele nu se potrivesc.\nTe rugăm să încerci din nou.",
    }

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email-ul este deja înregistrat.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set the username to the email
        if commit:
            user.save()
        return user
