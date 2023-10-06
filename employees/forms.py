from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from hr_dashboard.models import Department
from .models import Employee


class EmployeeSignUpForm(UserCreationForm):
    class Meta:
        model = Employee
        department = forms.ModelChoiceField(
            queryset=Department.objects.all(), required=False
        )
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "department",
        )


# Employee update details form
class EmployeeChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = Employee
        fields = (
            "email",
            "mobile_number",
            "bank",
            "account_name",
            "account_number",
        )
