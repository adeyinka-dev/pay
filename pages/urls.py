from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomePageView, Success
from employees.views import (
    EmployeePayslipListView,
    MyPayslipDetailView,
    SignUpView,
    EmployeeLoginView,
    EmployeeDashboardView,
    EmployeeUpdateView,
)
from hr_dashboard.views import (
    AdminLoginView,
    DeductionCreateView,
    DeductionListView,
    EmployeeDepartmentUpdateView,
    EmployeeListView,
    EmployeeDetailView,
    DepartmentCreateView,
    DepartmentListView,
    PayslipCreateView,
    PayslipDetailView,
    PayslipListView,
)
from django.contrib.auth.views import LoginView


urlpatterns = [
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
    path("", HomePageView.as_view(), name="home"),
    path("success/", Success.as_view(), name="success"),
    path(
        "login/",
        EmployeeLoginView.as_view(),
        name="login",
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user/", EmployeeDashboardView.as_view(), name="user"),
    path("update-details/", EmployeeUpdateView.as_view(), name="update_details"),
    path(
        "my-payslips/", EmployeePayslipListView.as_view(), name="employee_payslip_list"
    ),
    path(
        "my_payslips/<int:pk>/", MyPayslipDetailView.as_view(), name="my_payslip_detail"
    ),
    # HR Urls
    path("dashboard-login/", AdminLoginView.as_view(), name="admin_login"),
    path("dashboard/", EmployeeListView.as_view(), name="dashboard"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee_detail"),
    path("payslips/", PayslipListView.as_view(), name="payslip_list"),
    path("payslips/<int:pk>/", PayslipDetailView.as_view(), name="payslip_detail"),
    path("deductions/", DeductionListView.as_view(), name="deduction_list"),
    # HR forms
    path("departments/add/", DepartmentCreateView.as_view(), name="department_add"),
    path("departments/", DepartmentListView.as_view(), name="department_list"),
    path("payslips/add/", PayslipCreateView.as_view(), name="payslip_add"),
    path(
        "employees/<int:pk>/edit/",
        EmployeeDepartmentUpdateView.as_view(),
        name="employee_edit_department",
    ),
    path("deductions/add/", DeductionCreateView.as_view(), name="deduction_add"),
]
