from typing import Any
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
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
from .models import Deduction, Department, Payslip, VerificationCode
from .forms import (
    DeductionForm,
    DepartmentForm,
    EmployeeBasicSalaryForm,
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
        # Redirect to another URL if not a superuser
        return reverse("home")


class HRDashboardView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = "company/dashboard.html"

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
    success_url = reverse_lazy("verification_codes")


class VerificationCodeListView(ListView):
    model = VerificationCode
    template_name = "verification_codes.html"


class DepartmentListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Department
    template_name = "department_list.html"


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
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        # Set basic_salary_at_time_of_generation from the employee's current basic_salary
        payslip = form.save(
            commit=False
        )  # Get the Payslip object without saving to DB yet
        payslip.basic_salary_at_time_of_generation = payslip.employee.basic_salary
        payslip.save()  # Now, save the payslip to the DB
        messages.success(self.request, "Payslip created successfully!")
        return super().form_valid(form)


class PayslipListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Payslip
    template_name = "payslip_list.html"


class PayslipDetailView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    model = Payslip
    template_name = "payslip_detail.html"
    form_class = PayslipStatusForm

    def get_success_url(self):
        return reverse("dashboard")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(initial={"status": self.object.status})
        context["deductions"] = Deduction.objects.filter(
            employee=self.object.employee,
            month=self.object.month,
            year=self.object.year,
        )
        return context


class EmployeeProfileView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    model = Employee
    template_name = "employee_profile.html"
    context_object_name = "employee"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = EmployeeBasicSalaryForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = EmployeeBasicSalaryForm(request.POST, instance=self.object)

        if form.is_valid() and not self.object.is_salary_set:
            employee = form.save(commit=False)
            employee.is_salary_set = True
            employee.save()
            messages.success(request, "Basic salary set successfully!")
            return redirect("employee_profile", pk=employee.pk)

        messages.error(request, "Error setting salary. Maybe already set.")
        return self.render_to_response(self.get_context_data(form=form))
