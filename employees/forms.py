from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from hr_dashboard.models import Department
from .models import Employee


class EmployeeSignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, label="Full Name")

    class Meta:
        model = Employee
        fields = (
            "email",  # Use email instead of username
            "full_name",
            "password1",
            "password2",
        )

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        names = full_name.split()
        if len(names) < 2:
            raise ValidationError("Please enter both first and last name.")
        return full_name

    def save(self, commit=True):
        user = super().save(commit=False)
        names = self.cleaned_data["full_name"].split()
        user.first_name = names[0]
        user.last_name = " ".join(names[1:])
        if commit:
            user.save()
        return user


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
