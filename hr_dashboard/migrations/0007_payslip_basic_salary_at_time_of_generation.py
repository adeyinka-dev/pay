# Generated by Django 4.2.5 on 2023-10-15 22:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hr_dashboard", "0006_alter_deduction_month_alter_payslip_month_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="payslip",
            name="basic_salary_at_time_of_generation",
            field=models.DecimalField(decimal_places=2, max_digits=14, null=True),
        ),
    ]
