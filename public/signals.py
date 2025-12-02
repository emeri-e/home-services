from django.contrib.auth import get_user_model
from django_tenants.signals import post_schema_sync
from django.dispatch import receiver
from django_tenants.utils import schema_context

from .models import Client  # shared tenant model

User = get_user_model()

@receiver(post_schema_sync, sender=Client)
def create_tenant_superuser(sender, tenant, **kwargs):
    """
    Run inside the tenant's schema to create tenant-specific user(s).
    """
    schema_name = tenant.schema_name
    # explicitly switch to tenant schema
    with schema_context(schema_name):
        # double-check user existence inside tenant schema
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password="admin123", email="")
            print(f"✅ Superuser created for schema: {schema_name}")
        else:
            print(f"⚠️ Superuser already exists in schema: {schema_name}, skipping.")
