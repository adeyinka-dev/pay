from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee


class EmployeeSignUpForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = (
            "first_name",
            "last_name",
            "email",
        )


# Employee update details form
class EmployeeChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = (
            "email",
            "mobile_number",
            "bank",
            "account_name",
            "account_number",
        )
