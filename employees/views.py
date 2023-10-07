from datetime import datetime
from .models import Employee
from .forms import EmployeeSignUpForm, EmployeeChangeForm
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


class EmployeeLoginView(auth_views.LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        return reverse_lazy("user")


class SignUpView(CreateView):
    form_class = EmployeeSignUpForm
    template_name = "registration/signup.html"

    def generate_unique_employee_id(self):
        year_part = str(datetime.now().year)[2:]
        while True:
            random_part = f"{random.randint(0, 9999):04}"  # This ensures the number is always 4 digits
            new_id = f"{year_part}{random_part}"
            if not Employee.objects.filter(employee_id=new_id).exists():
                return new_id

    def form_valid(self, form):
        user = form.save(commit=False)  # Don't save the instance yet
        user.username = user.email  # Set the username to the email
        user.employee_id = self.generate_unique_employee_id()
        # If the department field is empty, it will simply save as None
        user.department = form.cleaned_data.get("department")
        user.save()
        messages.success(self.request, "Thank You")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("success")


class EmployeeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Payslip = apps.get_model("hr_dashboard", "Payslip")
        context["last_three_payslips"] = Payslip.objects.filter(
            employee=self.request.user
        ).order_by("-date")[:3]
        return context


class EmployeePayslipListView(LoginRequiredMixin, ListView):
    model = Payslip
    template_name = "employee_payslip_list.html"

    def get_queryset(self):
        return Payslip.objects.filter(employee=self.request.user).order_by("-date")


class MyPayslipDetailView(LoginRequiredMixin, DetailView):
    model = Payslip
    template_name = "my_payslip_details.html"


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeChangeForm
    template_name = "update_details.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("success")
