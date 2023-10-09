from django.db import models
from django.urls import reverse
from employees.models import Employee
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


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
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    month = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 13)], null=True
    )
    year = models.PositiveIntegerField(default=timezone.now().year, null=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.description}"


class Payslip(models.Model):
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    PENDING = "PEN"
    UNPAID = "UNP"
    PAID = "PAID"
    STATUS = [(PENDING, "Pending"), (UNPAID, "Unpaid"), (PAID, "Paid")]
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    month = models.PositiveIntegerField(choices=MONTH_CHOICES, null=True, blank=True)
    year = models.PositiveIntegerField(
        default=timezone.now().year, null=True, blank=True
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
        return self.employee.basic_salary + self.bonuses - self.total_deductions

    def __str__(self):
        payslip_id = f"{self.employee.id}-{self.month:02}-{str(self.year)[2:]}"
        return f"{self.employee.first_name} {self.employee.last_name} - {self.date} - Net Pay:{self.net_pay} - Payslip ID:{payslip_id}"

    def get_absolute_url(self):
        return reverse("payslip", kwargs={"pk": self.pk})
