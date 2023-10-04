from django.urls import path
from .views import HomePageView
from employees.views import SignUpView
from django.contrib.auth.views import LoginView


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
]
