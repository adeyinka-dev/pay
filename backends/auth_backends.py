from django.contrib.auth.backends import ModelBackend
from employees.models import Employee
from django.contrib.auth.models import User


class EmailOrEmployeeIDBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to fetch the user by email
            user = Employee.objects.get(email=username)
            if user.check_password(password):
                return user
        except Employee.DoesNotExist:
            try:
                # Try to fetch the user by employee_id
                user = Employee.objects.get(employee_id=username)
                if user.check_password(password):
                    return user
            except Employee.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return Employee.objects.get(pk=user_id)
        except Employee.DoesNotExist:
            return None


class EmployeeBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Employee.objects.get(username=username)
            if user.check_password(password):
                return user
        except Employee.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Employee.objects.get(pk=user_id)
        except Employee.DoesNotExist:
            return None


class AdminUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
