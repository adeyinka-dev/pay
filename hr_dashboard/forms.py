from django import forms
from .models import Deduction, Department, Payslip
from employees.models import Employee


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name"]


class EmployeeDepartmentForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = Employee
        fields = ["department"]


class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = ["type", "description", "amount"]


class PayslipForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = ["employee", "month", "year", "bonuses"]
