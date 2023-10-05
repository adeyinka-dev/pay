from django.contrib import admin

from .models import Department, Payslip, Deduction

admin.site.register(Department)
admin.site.register(Payslip)
admin.site.register(Deduction)
