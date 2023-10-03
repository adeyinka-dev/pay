from django.test import TestCase

from django.contrib.auth import get_user_model


class EmployeeTests(TestCase):
    def test_create_user(self):
        Employee = get_user_model()
        employee = Employee.objects.create_user(
            username="testuser1",
            first_name="test1",
            last_name="user",
            email="test1@mail.com",
            password="testpass12345",
        )
        self.assertEqual(employee.username, "testuser1")
        self.assertEqual(employee.first_name, "test1")
        self.assertEqual(employee.last_name, "user")
        self.assertEqual(employee.email, "test1@mail.com")
