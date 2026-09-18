from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class StudentSignupForm(UserCreationForm):
    """Public signup form. Anyone who signs up here is a student account
    (is_staff stays False) — admin accounts are created separately via
    `manage.py createsuperuser` or promoted in the Django admin."""

    first_name = forms.CharField(max_length=150, required=True, label='First name')
    last_name = forms.CharField(max_length=150, required=False, label='Last name')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
