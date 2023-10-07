from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from hr_dashboard.models import Department
from .models import Employee


class EmployeeSignUpForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = (
            "email",  # Use email instead of username
            "first_name",
            "last_name",
            "department",
            "password1",
            "password2",
        )


# Employee update details form
class EmployeeChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = Employee
        fields = (
            "mobile_number",
            "bank",
            "account_name",
            "account_number",
        )
