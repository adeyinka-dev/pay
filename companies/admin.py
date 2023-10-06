from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Client
from django.contrib.auth.models import User
from django_tenants.utils import schema_context
from django.contrib import messages
from django.db import connection


def create_client_superuser(modeladmin, request, queryset):
    for client in queryset:
        with schema_context(client.schema_name):
            # Check if superuser exists for this tenant
            if User.objects.filter(is_superuser=True).exists():
                # Display error message
                messages.error(
                    request, f"Client {client.name} already has a superuser."
                )
            else:
                # define a fixed username/password for the superuser,
                # or derive it from the Client model properties.
                User.objects.create_superuser(
                    username="admin",
                    password="adminpassword",
                    email=client.email,
                )
                messages.success(
                    request, f"Superuser created for Client {client.name}."
                )


create_client_superuser.short_description = "Create superuser for selected company"


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ["name"]
    actions = [create_client_superuser]

    def in_public_schema(self):
        return connection.schema_name == "public"

    def has_module_permission(self, request):
        return self.in_public_schema()

    def has_view_permission(self, request, obj=None):
        return self.in_public_schema()

    def has_change_permission(self, request, obj=None):
        return self.in_public_schema()

    def has_add_permission(self, request, obj=None):
        return self.in_public_schema()

    def has_delete_permission(self, request, obj=None):
        return self.in_public_schema()
