# Generated by Django 4.2.5 on 2023-10-15 22:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employees", "0006_employee_basic_salary_alter_employee_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="home_address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="is_salary_set",
            field=models.BooleanField(default=False),
        ),
    ]