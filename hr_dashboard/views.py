from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from employees.models import Employee
from .models import Deduction, Department, Payslip
from .forms import DeductionForm, DepartmentForm, EmployeeDepartmentForm, PayslipForm


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "department_form.html"
    success_url = reverse_lazy("department_list")


class DepartmentListView(ListView):
    model = Department
    template_name = "department_list.html"


class EmployeeDepartmentUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeDepartmentForm
    template_name = "employee_department_form.html"
    success_url = reverse_lazy("dashboard")


class DeductionCreateView(CreateView):
    model = Deduction
    form_class = DeductionForm
    template_name = "deduction_form.html"
    success_url = reverse_lazy("deduction_list")


class DeductionListView(ListView):
    model = Deduction
    template_name = "deduction_list.html"


class PayslipCreateView(CreateView):
    model = Payslip
    form_class = PayslipForm
    template_name = "payslip_form.html"
    success_url = reverse_lazy("payslip_list")


class PayslipListView(ListView):
    model = Payslip
    template_name = "payslip_list.html"


class PayslipDetailView(DetailView):
    model = Payslip
    template_name = "payslip_detail.html"


class EmployeeListView(ListView):
    model = Employee
    template_name = "dashboard.html"


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = "employee_detail.html"
