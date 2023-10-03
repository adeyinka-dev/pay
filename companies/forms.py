from django import forms
from .models import Client


# Client Creation form
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "schema_name",
        ]
