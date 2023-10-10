from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from employees.models import Employee
from .models import Deduction, Department, Payslip
from .forms import DeductionForm, DepartmentForm, EmployeeDepartmentForm, PayslipForm
from django.contrib.auth.views import LoginView
from django.urls import reverse


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class AdminLoginView(LoginView):
    template_name = "admin_login.html"

    def get_success_url(self):
        # Check if the user is a superuser
        if self.request.user.is_superuser:
            return reverse("dashboard")
        # Redirect to another URL if not a superuser (optional)
        return reverse("home")


class DepartmentCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "department_form.html"
    success_url = reverse_lazy("department_list")


class DepartmentListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Department
    template_name = "department_list.html"


class EmployeeDepartmentUpdateView(
    LoginRequiredMixin, SuperuserRequiredMixin, UpdateView
):
    model = Employee
    form_class = EmployeeDepartmentForm
    template_name = "employee_department_form.html"
    success_url = reverse_lazy("dashboard")


class DeductionCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Deduction
    form_class = DeductionForm
    template_name = "deduction_form.html"
    success_url = reverse_lazy("deduction_list")


class DeductionListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Deduction
    template_name = "deduction_list.html"


class PayslipCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Payslip
    form_class = PayslipForm
    template_name = "payslip_form.html"
    success_url = reverse_lazy("payslip_list")


class PayslipListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Payslip
    template_name = "payslip_list.html"


class PayslipDetailView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    model = Payslip
    template_name = "payslip_detail.html"


class EmployeeListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Employee
    template_name = "dashboard.html"


# class EmployeeDetailView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
#     model = Employee
#     template_name = "employee_detail.html"
