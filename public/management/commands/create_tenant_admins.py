from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from django.contrib.auth import get_user_model
from public.models import Client

User = get_user_model()


class Command(BaseCommand):
    help = "Create 'admin' superuser inside every tenant schema if missing."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🔍 Scanning tenants..."))

        tenants = Client.objects.all().order_by("schema_name")

        if not tenants.exists():
            self.stdout.write(self.style.WARNING("No tenants found."))
            return

        for tenant in tenants:
            schema = tenant.schema_name
            self.stdout.write(f"\n➡️  Processing tenant schema: {schema}")

            with schema_context(schema):
                if User.objects.filter(username="admin").exists():
                    self.stdout.write(self.style.WARNING(f"   ⚠️  'admin' already exists → SKIPPED"))
                    continue
                
                User.objects.create_superuser(
                    username="admin",
                    password="admin1234",
                    email=""
                )
                self.stdout.write(self.style.SUCCESS(f"   ✅ Created admin in schema '{schema}'"))

        self.stdout.write(self.style.SUCCESS("\n🎉 Done creating tenant admins!"))
