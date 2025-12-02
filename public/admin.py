from django_tenants.admin import TenantAdminMixin
from .models import Client, Domain
from django.contrib import admin
from django.contrib.admin import AdminSite

class SuperAdminSite(AdminSite):
    site_header = "Platform Admin"
    site_title = "Platform Admin"
    index_title = "Platform Administration"

super_admin_site = SuperAdminSite(name="super_admin")



class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'created_on')
    search_fields = ('name', 'schema_name')

class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    search_fields = ('domain',)

super_admin_site.register(Client, ClientAdmin)
super_admin_site.register(Domain, DomainAdmin)
