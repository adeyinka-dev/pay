from django import forms
from .models import Client
from django.contrib.auth.models import User
from django_tenants.utils import schema_context


class ClientForm(forms.ModelForm):
    admin_password = forms.CharField(
        widget=forms.PasswordInput(), label="Admin Password"
    )

    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "schema_name",
            "admin_password",  # add this if you want to collect a password
        ]

    def save(self, commit=True):
        # First, save the Client instance
        client = super(ClientForm, self).save(commit=commit)

        # Now, create the superuser for this client
        with schema_context(client.schema_name):
            User.objects.create_superuser(
                username=client.email,
                password=self.cleaned_data["admin_password"],
                email=client.email,
            )

        return client
