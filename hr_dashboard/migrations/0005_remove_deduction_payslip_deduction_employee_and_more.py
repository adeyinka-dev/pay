# Generated by Django 4.2.5 on 2023-10-09 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("employees", "0006_employee_basic_salary_alter_employee_department"),
        ("hr_dashboard", "0004_remove_department_standard_wages_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="deduction",
            name="payslip",
        ),
        migrations.AddField(
            model_name="deduction",
            name="employee",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="employees.employee",
            ),
        ),
        migrations.AddField(
            model_name="deduction",
            name="month",
            field=models.PositiveIntegerField(
                choices=[
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7),
                    (8, 8),
                    (9, 9),
                    (10, 10),
                    (11, 11),
                    (12, 12),
                ],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="deduction",
            name="year",
            field=models.PositiveIntegerField(default=2023, null=True),
        ),
    ]
