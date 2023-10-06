from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Client
from django.contrib.auth.models import User
from django_tenants.utils import schema_context
from django.contrib import messages
from django.db import connection


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ["name"]

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
