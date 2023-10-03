from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator


class Employee(AbstractUser):
    mobile_number = models.PositiveBigIntegerField(blank=True, null=True)
    bank = models.ForeignKey("banklist_api.Bank", on_delete=models.SET_NULL, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
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