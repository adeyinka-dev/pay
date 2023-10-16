from django.contrib import admin

from .models import Department, Payslip, Deduction, VerificationCode

admin.site.register(Department)
admin.site.register(Payslip)
admin.site.register(Deduction)
admin.site.register(VerificationCode)
