from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "mobile_number",
        "bank",
        "account_name",
        "account_number",
    ]
    search_fields = [
        "username",
        "email",
    ]
