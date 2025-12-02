from django.core.management.base import BaseCommand
from public.models import Client, Domain

class Command(BaseCommand):
    help = "Create the default domain for the public tenant if it does not exist."

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='localhost',
            help='The domain to use for the public tenant'
        )

    def handle(self, *args, **options):
        # Get or create public tenant
        public_tenant, created = Client.objects.get_or_create(
            schema_name='public',
            defaults={'name': 'Platform'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS("✅ Created public tenant"))

        # Check if a domain exists for public
        domain_name = options['domain']
        domain, created = Domain.objects.get_or_create(
            tenant=public_tenant,
            defaults={'domain': domain_name}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Created default domain '{domain.domain}' for public tenant"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Domain already exists: {domain.domain}"))

