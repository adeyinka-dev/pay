from rest_framework import generics
from .models import Bank
from .serializers import BankSerializer


class BankAPIView(generics.ListAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
