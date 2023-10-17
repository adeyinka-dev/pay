from django import forms
from .models import Deduction, Department, Payslip
from employees.models import Employee
from django.core.exceptions import ValidationError


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "row", "basic_pay"]


class EmployeeBasicSalaryForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["basic_salary"]


class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = ["type", "description", "amount", "employee", "year", "month"]

    # This method should be at the DeductionForm level, not inside the Meta class
    def clean(self):
        cleaned_data = super().clean()  # Changed this line for a more modern approach
        employee = cleaned_data.get("employee")
        month = cleaned_data.get("month")
        year = cleaned_data.get("year")

        if (
            employee
            and month
            and year
            and Payslip.objects.filter(
                employee=employee, month=month, year=year
            ).exists()
        ):
            raise forms.ValidationError(  # Note the changed ValidationError import
                "A payslip has already been generated for this employee for the selected month and year. Deduction cannot be added."
            )
        return cleaned_data


class PayslipForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = ["employee", "month", "year", "bonuses"]


class PayslipStatusForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = ["status"]

    def clean_status(self):
        new_status = self.cleaned_data.get("status")
        instance = getattr(self, "instance", None)
        if instance and instance.status == "Paid" and instance.status != new_status:
            raise forms.ValidationError("")
        return new_status
