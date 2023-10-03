# admin.py

from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "full_name",
        "mobile_number",
        "bank_name",
        "account_name",
        "account_number",
    ]
    search_fields = ["username", "email", "full_name"]
