from typing import Any
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db import models
from django.db.models import Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView,
)
from employees.models import Employee
from .models import Deduction, Department, Payslip
from .forms import (
    DeductionForm,
    DepartmentForm,
    EmployeeDepartmentForm,
    PayslipForm,
    PayslipStatusForm,
)
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


class HRDashboardView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_employees"] = Employee.objects.count()
        total_payouts = sum([p.net_pay for p in Payslip.objects.filter(status="Paid")])
        context["total_payouts"] = total_payouts
        total_pending = sum(
            [p.net_pay for p in Payslip.objects.filter(status="Pending")]
        )
        context["total_pending"] = total_pending
        total_deduction = sum(
            [d.total_deductions for d in Payslip.objects.filter(status="Paid")]
        )
        context["total_deductions"] = total_deduction
        context["latest_payslips"] = Payslip.objects.all()[:5]
        context["new_employees"] = Employee.objects.order_by("-date_joined")[:5]
        return context


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


class PayslipDetailView(
    LoginRequiredMixin, SuperuserRequiredMixin, FormMixin, DetailView
):
    model = Payslip
    template_name = "payslip_detail.html"
    form_class = PayslipStatusForm

    def get_success_url(self):
        return reverse("dashboard")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        payslip = self.get_object()
        payslip.status = form.cleaned_data["status"]
        payslip.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["deductions"] = Deduction.objects.filter(
            employee=self.object.employee,
            month=self.object.month,
            year=self.object.year,
        )
        return context


class EmployeeListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Employee
    template_name = "dashboard.html"
