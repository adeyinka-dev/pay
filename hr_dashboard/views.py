from typing import Any
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.db import models
from django.db.models import Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.edit import FormMixin
from django.contrib.auth import views as auth_views
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
        context["latest_payslips"] = Payslip.objects.order_by("-generated_on")[:5]
        context["new_employees"] = Employee.objects.order_by("-date_joined")[:5]
        return context


class AdminLogoutView(auth_views.LogoutView):
    next_page = "admin_login"


class CombinedDepartmentView(LoginRequiredMixin, SuperuserRequiredMixin, View):
    template_name = "company/department.html"

    def get(self, request, *args, **kwargs):
        form = DepartmentForm()
        departments = Department.objects.all()
        issued_codes = VerificationCode.objects.filter(status="Issued").order_by("-id")[
            :4
        ]
        context = {
            "form": form,
            "departments": departments,
            "issued_codes": issued_codes,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("department"))
        departments = Department.objects.all()
        context = {
            "form": form,
            "departments": departments,
        }
        return render(request, self.template_name, context)


class VerificationCodeListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = VerificationCode
    template_name = "verification_codes.html"


class VerificationCodeByDepartmentListView(
    LoginRequiredMixin, SuperuserRequiredMixin, ListView
):
    model = VerificationCode
    template_name = "company/codes_by_department.html"

    def get_queryset(self):
        department_name = self.kwargs.get("department_name")
        department = Department.objects.get(name=department_name)
        return department.verification_codes.filter(status=VerificationCode.UNUSED)


class EmployeeListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Employee
    template_name = "company/employee_list.html"


class DeductionCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Deduction
    form_class = DeductionForm
    template_name = "company/deduction_form.html"
    success_url = reverse_lazy("deduction_list")


class DeductionListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Deduction
    template_name = "company/deduction_list.html"

    def get_queryset(self):
        return Deduction.objects.all().order_by("-created_at")


class PayslipCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Payslip
    form_class = PayslipForm
    template_name = "company/generate_payslip.html"
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
    template_name = "company/payslip_list.html"
    ordering = ["-generated_on"]


class PayslipDetailView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    model = Payslip
    template_name = "company/payslip_details.html"
    form_class = PayslipStatusForm

    def get_success_url(self):
        return reverse("dashboard")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)

        error_message = None  # Initialize the error message as None

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            if form.errors.get("status"):
                # Define the error message if there's an error related to the status field
                error_message = "Once a payslip is set as paid, it cannot be changed."

        return self.render_to_response(
            self.get_context_data(form=form, error_message=error_message)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(initial={"status": self.object.status})
        context["deductions"] = Deduction.objects.filter(
            employee=self.object.employee,
            month=self.object.month,
            year=self.object.year,
        )
        context["error_message"] = kwargs.get("error_message", None)
        return context


class EmployeeProfileView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    model = Employee
    template_name = "company/employee_profile.html"
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
