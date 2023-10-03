from django.urls import path
from .views import BankAPIView

urlpatterns = [
    path("", BankAPIView.as_view(), name="bank_list"),
]
