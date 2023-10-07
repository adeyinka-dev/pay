from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator


# generate an employee ID - last 2 digit of current year and 4 random numbers
class Employee(AbstractUser):
    email = models.EmailField(unique=True)
    employee_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
    mobile_number = models.PositiveBigIntegerField(blank=True, null=True)
    bank = models.ForeignKey("banklist_api.Bank", on_delete=models.SET_NULL, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(
        "hr_dashboard.Department", on_delete=models.SET_NULL, null=True, blank=True
    )
    account_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^\d{10}$",
                message="Account number must be exactly 10 digits",
                code="invalid_account_number",
            )
        ],
    )

    # Override the groups and user_permissions fields
    groups = models.ManyToManyField(Group, blank=True, related_name="employee_set")
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="employee_set"
    )
