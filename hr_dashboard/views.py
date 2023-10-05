from django.shortcuts import render
from django.views.generic import ListView
from employees.models import Employee


class EmployeeListView(ListView):
    model = Employee
    template_name = "dashboard.html"
