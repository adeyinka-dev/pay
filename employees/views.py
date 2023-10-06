from datetime import datetime
from .models import Employee
from .forms import EmployeeSignUpForm, EmployeeChangeForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, UpdateView
import random
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin


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


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeChangeForm
    template_name = "update_details.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("success")
