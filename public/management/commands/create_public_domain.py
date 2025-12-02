from django.core.management.base import BaseCommand
from public.models import Client, Domain

class Command(BaseCommand):
    help = "Create the default domain for the public tenant if it does not exist."

    def handle(self, *args, **options):
        # Get or create public tenant
        public_tenant, created = Client.objects.get_or_create(
            schema_name='public',
            defaults={'name': 'Platform'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✅ Created public tenant"))

        # Check if a domain exists for public
        domain, created = Domain.objects.get_or_create(
            tenant=public_tenant,
            defaults={'domain': 'localhost'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Created default domain 'localhost' for public tenant"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Domain already exists: {domain.domain}"))

