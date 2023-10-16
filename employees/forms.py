from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from hr_dashboard.models import Department, VerificationCode
from .models import Employee


class EmployeeSignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, label="Full Name")
    verification_code = forms.CharField()

    class Meta:
        model = Employee
        fields = (
            "email",
            "full_name",
            "verification_code",
            "password1",
            "password2",
        )

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        names = full_name.split()
        if len(names) < 2:
            raise ValidationError("Please enter both first and last name.")
        return full_name

    def clean_verification_code(self):
        code = self.cleaned_data.get("verification_code")
        try:
            verification_code_instance = VerificationCode.objects.get(code=code)
        except VerificationCode.DoesNotExist:
            raise forms.ValidationError("Invalid verification code.")
        if verification_code_instance.status == VerificationCode.ISSUED:
            raise forms.ValidationError("This verification code has already been used.")

        return code

    def save(self, commit=True):
        user = super().save(
            commit=False
        )  # Prepare the user instance but don't save to DB yet
        names = self.cleaned_data["full_name"].split()
        user.first_name = names[0]
        user.last_name = " ".join(names[1:])
        return user


# Employee bank details form
class EmployeeBankDetailsForm(UserChangeForm):
    password = None

    class Meta:
        model = Employee
        fields = (
            "bank",
            "account_name",
            "account_number",
        )
