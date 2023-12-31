import uuid
from django.db import models
from django.urls import reverse
from employees.models import Employee
from django.utils import timezone


MONTH_CHOICES = [
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
]

"""Creating a Departemnt will generate multiple unique codes that will be used for verifcation on sign up"""


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    row = models.IntegerField()
    basic_pay = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, null=True, blank=True
    )

    def get_verification_codes(self):
        return self.verification_codes.all()

    def save(self, *args, **kwargs):
        # Check if the instance already exists in the database
        if self.pk:
            old_department = Department.objects.get(pk=self.pk)
            difference = self.row - old_department.row
        else:
            difference = self.row

        super().save(*args, **kwargs)

        # Only create additional VerificationCode instances if there's an increase
        if difference > 0:
            for _ in range(difference):
                VerificationCode.objects.create(
                    department=self, code=str(uuid.uuid4())[:8]
                )


class VerificationCode(models.Model):
    UNUSED = "Unused"
    ISSUED = "Issued"
    STATUS_CHOICES = [
        (UNUSED, "Unused"),
        (ISSUED, "Issued"),
    ]

    department = models.ForeignKey(
        Department, related_name="verification_codes", on_delete=models.CASCADE
    )
    code = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=UNUSED)
    used_by = models.OneToOneField(
        Employee, null=True, blank=True, on_delete=models.SET_NULL
    )


class Deduction(models.Model):
    TAX = "TAX"
    DEBT = "DEBT"
    ABSENCE = "ABSENCE"
    TURNOVER = "TURNOVER"
    SALARY_ADVANCE = "SALARY_ADVANCE"
    OTHERS = "OTHERS"

    DEDUCTION_TYPES = [
        (TAX, "Tax"),
        (DEBT, "Shortfall"),
        (ABSENCE, "Absence Penalty"),
        (SALARY_ADVANCE, "Salary Advance"),
        (OTHERS, "Others"),
    ]
    type = models.CharField(max_length=20, choices=DEDUCTION_TYPES)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveIntegerField(choices=MONTH_CHOICES)
    year = models.PositiveIntegerField(default=timezone.now().year)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.description}"


class Payslip(models.Model):
    PENDING = "Pending"
    UNPAID = "Unpaid"
    PAID = "Paid"
    STATUS = [(PENDING, "Pending"), (UNPAID, "Unpaid"), (PAID, "Paid")]

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    month = models.PositiveIntegerField(choices=MONTH_CHOICES, null=True, blank=True)
    year = models.PositiveIntegerField(
        default=timezone.now().year, null=True, blank=True
    )

    basic_salary_at_time_of_generation = models.DecimalField(
        max_digits=14, decimal_places=2
    )
    bonuses = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default=PENDING)

    class Meta:
        unique_together = ["employee", "month", "year"]

    @property
    def total_deductions(self):
        deductions_for_month = Deduction.objects.filter(
            employee=self.employee, month=self.month, year=self.year
        )
        total = deductions_for_month.aggregate(sum=models.Sum("amount"))["sum"] or 0
        return total

    @property
    def net_pay(self):
        basic_salary = self.basic_salary_at_time_of_generation or 0
        return basic_salary + self.bonuses - self.total_deductions

    def get_payslip_id(self):
        return f"{self.employee.employee_id}{self.month:02}{str(self.year)[2:]}"

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.date} - Net Pay:{self.net_pay} - Payslip ID:{self.get_payslip_id()}"

    def get_absolute_url(self):
        return reverse("payslip", kwargs={"pk": self.pk})
