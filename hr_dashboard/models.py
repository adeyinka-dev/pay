from django.db import models
from employees.models import Employee


class Department(models.Model):
    name = models.CharField(max_length=100)
    standard_wages = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}"


class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    month = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 13)], null=True, blank=True
    )  # 1-12 for January to December
    year = models.PositiveIntegerField(null=True, blank=True)
    earnings = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    bonuses = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        unique_together = ["employee", "month", "year"]

    @property
    def total_deductions(self):
        return self.deduction_set.aggregate(sum=models.Sum("amount"))["sum"] or 0

    @property
    def net_pay(self):
        return self.earnings + self.bonuses - self.total_deductions

    def __str__(self):
        return f"{self.employee.username} - {self.date} - Net Pay:{self.net_pay}"


class Deduction(models.Model):
    TAX = "TAX"
    DEBT = "DEBT"
    ABSENCE = "ABSENCE"
    TURNOVER = "TURNOVER"
    SALARY_ADVANCE = "SALARY_ADVANCE"

    DEDUCTION_TYPES = [
        (TAX, "Tax"),
        (DEBT, "Shortfall"),
        (ABSENCE, "Absence Penalty"),
        (SALARY_ADVANCE, "Salary Advance"),
    ]
    payslip = models.ForeignKey(Payslip, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=DEDUCTION_TYPES)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.get_type_display()} - {self.description}"
