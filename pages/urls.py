from django.urls import path
from .views import HomePageView, Success
from employees.views import SignUpView, EmployeeLoginView, EmployeeDashboardView
from hr_dashboard.views import (
    EmployeeListView,
    EmployeeDetailView,
    DepartmentCreateView,
    DepartmentListView,
)
from django.contrib.auth.views import LoginView


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("success/", Success.as_view(), name="success"),
    path(
        "login/",
        EmployeeLoginView.as_view(),
        name="login",
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user/", EmployeeDashboardView.as_view(), name="user"),
    # HR Urls
    path("dashboard/", EmployeeListView.as_view(), name="dashboard"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee_detail"),
    # HR forms
    path("departments/add/", DepartmentCreateView.as_view(), name="department_add"),
    path("departments/", DepartmentListView.as_view(), name="department_list"),
]
