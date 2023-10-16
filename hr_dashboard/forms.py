from django import forms
from .models import Deduction, Department, Payslip
from employees.models import Employee


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "row"]


class EmployeeBasicSalaryForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["basic_salary"]


class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = ["type", "description", "amount", "employee", "year", "month"]


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
            raise forms.ValidationError(
                "Once a payslip is set as paid, it cannot be changed."
            )
        return new_status
