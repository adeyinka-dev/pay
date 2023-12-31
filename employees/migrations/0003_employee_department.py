# Generated by Django 4.2.5 on 2023-10-05 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("hr_dashboard", "0002_alter_deduction_type"),
        (
            "employees",
            "0002_remove_employee_bank_name_remove_employee_full_name_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="hr_dashboard.department",
            ),
        ),
    ]
