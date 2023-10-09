# Generated by Django 4.2.5 on 2023-10-09 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("employees", "0006_employee_basic_salary_alter_employee_department"),
        ("hr_dashboard", "0003_alter_payslip_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="department",
            name="standard_wages",
        ),
        migrations.RemoveField(
            model_name="payslip",
            name="department",
        ),
        migrations.RemoveField(
            model_name="payslip",
            name="earnings",
        ),
        migrations.AddField(
            model_name="payslip",
            name="status",
            field=models.CharField(
                choices=[("PEN", "Pending"), ("UNP", "Unpaid"), ("PAID", "Paid")],
                default="PEN",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="payslip",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="payslip",
            name="employee",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="employees.employee",
            ),
        ),
        migrations.AlterField(
            model_name="payslip",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2023, null=True),
        ),
    ]
