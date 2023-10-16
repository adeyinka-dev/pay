from datetime import datetime

from hr_dashboard.models import VerificationCode
from .models import Employee
from .forms import EmployeeSignUpForm, EmployeeBankDetailsForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, UpdateView, ListView, DetailView
import random
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps

Payslip = apps.get_model("hr_dashboard", "Payslip")
Deduction = apps.get_model("hr_dashboard", "Deduction")


class EmployeeHomePageView(TemplateView):
    template_name = "employee/employee_home.html"


class EmployeeLoginView(auth_views.LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        return reverse_lazy("employee_dashboard")


class SignUpView(CreateView):
    form_class = EmployeeSignUpForm
    template_name = "registration/signup.html"

    def generate_unique_employee_id(self):
        year_part = str(datetime.now().year)[2:]
        while True:
            random_part = f"{random.randint(0, 9999):04}"  # Ensure a 4-digit number
            new_id = f"{year_part}{random_part}"
            if not Employee.objects.filter(employee_id=new_id).exists():
                return new_id

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email  # Set username to email
        user.employee_id = self.generate_unique_employee_id()

        # Fetch the verification code instance
        code_instance = VerificationCode.objects.get(
            code=form.cleaned_data.get("verification_code")
        )
        user.department = code_instance.department  # Assign the department

        user.save()  # Save user to DB

        # Update VerificationCode instance
        code_instance.used_by = user
        code_instance.status = VerificationCode.ISSUED
        code_instance.save()

        messages.success(self.request, "Thank You")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("success")


class EmployeeLogoutView(auth_views.LogoutView):
    next_page = "employee_home"


class EmployeeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "employee/employee_dashboard.html"


class EmployeeProfileView(LoginRequiredMixin, TemplateView):
    template_name = "employee/employee_details.html"


class EmployeePayslipListView(LoginRequiredMixin, ListView):
    model = Payslip
    template_name = "employee/employee_payslip_list.html"

    def get_queryset(self):
        return Payslip.objects.filter(employee=self.request.user).order_by("-date")


class MyPayslipDetailView(LoginRequiredMixin, DetailView):
    model = Payslip
    template_name = "employee/my_payslip_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_name"] = self.request.tenant.name
        context["deductions"] = Deduction.objects.filter(
            employee=self.object.employee,
            month=self.object.month,
            year=self.object.year,
        )
        return context


class EmployeeBankUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeBankDetailsForm
    template_name = "employee/update_bank_details.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("success")
