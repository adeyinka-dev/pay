from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomePageView, Success
from employees.views import (
    EmployeeLogoutView,
    EmployeePayslipListView,
    MyPayslipDetailView,
    SignUpView,
    EmployeeLoginView,
    EmployeeDashboardView,
    EmployeeBankUpdateView,
    EmployeeHomePageView,
    EmployeeProfileView,
)

from hr_dashboard.views import (
    AdminLoginView,
    AdminLogoutView,
    CombinedDepartmentView,
    HRDashboardView,
    EmployeeListView,
    # Unfixed
    DeductionCreateView,
    DeductionListView,
    EmployeeProfileView,
    VerificationCodeByDepartmentListView,
    VerificationCodeListView,
    PayslipCreateView,
    PayslipDetailView,
    PayslipListView,
)
from django.contrib.auth.views import LoginView


urlpatterns = [
    # Employee URLS
    path("employee/", EmployeeHomePageView.as_view(), name="employee_home"),
    path("signup/", SignUpView.as_view(), name="employee_signup"),
    path(
        "employee-login/",
        EmployeeLoginView.as_view(),
        name="employee_login",
    ),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("userlogout/", EmployeeLogoutView.as_view(), name="employee_logout"),
    path("your-dashboard/", EmployeeDashboardView.as_view(), name="employee_dashboard"),
    path("my-profile/", EmployeeProfileView.as_view(), name="employee_details"),
    path("user/", EmployeeDashboardView.as_view(), name="user"),
    path(
        "update-bank-details/",
        EmployeeBankUpdateView.as_view(),
        name="update_bank_details",
    ),
    path(
        "my-payslips/", EmployeePayslipListView.as_view(), name="employee_payslip_list"
    ),
    path(
        "my_payslip/<int:pk>/", MyPayslipDetailView.as_view(), name="my_payslip_detail"
    ),
    # HR Urls
    path("home/", HomePageView.as_view(), name="home"),
    path("success/", Success.as_view(), name="success"),
    path("", AdminLoginView.as_view(), name="admin_login"),
    path("dashboard/", HRDashboardView.as_view(), name="dashboard"),
    path("adminlogout/", AdminLogoutView.as_view(), name="admin_logout"),
    path("employee-registry/", EmployeeListView.as_view(), name="admin_employee_list"),
    path(
        "adminview-employees/<int:pk>/",
        EmployeeProfileView.as_view(),
        name="employee_profile",
    ),
    path(
        "departments/",
        CombinedDepartmentView.as_view(),
        name="department",
    ),
    path(
        "verification-codes/",
        VerificationCodeListView.as_view(),
        name="verification_codes",
    ),
    path(
        "verification_codes/<str:department_name>/",
        VerificationCodeByDepartmentListView.as_view(),
        name="codes_by_department",
    ),
    path("deductions/add/", DeductionCreateView.as_view(), name="deduction_add"),
    path("deductions/", DeductionListView.as_view(), name="deduction_list"),
    path("payslips/generate/", PayslipCreateView.as_view(), name="generate_payslip"),
    path("payslips/<int:pk>/", PayslipDetailView.as_view(), name="payslip_detail"),
    path("dashboard/payslips-list", PayslipListView.as_view(), name="all_payslip_list"),
]
