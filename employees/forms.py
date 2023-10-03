# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee


class EmployeeSignUpForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "full_name",
            "mobile_number",
            "bank_name",
            "account_name",
            "account_number",
        )
