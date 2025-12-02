from django.core.management.base import BaseCommand, CommandError
from django_tenants.utils import schema_context

from public.models import Client, Domain


class Command(BaseCommand):
    help = "Populate core and booking models for a tenant (by schema or domain)."

    def add_arguments(self, parser):
        parser.add_argument('--schema', dest='schema', help='Tenant schema name to populate')
        parser.add_argument('--domain', dest='domain', help='Domain name to find tenant and populate')

    def handle(self, *args, **options):
        schema = options.get('schema')
        domain = options.get('domain')

        if not schema and not domain:
            raise CommandError("Provide either --schema or --domain to select a tenant.")

        tenant = None
        if domain:
            try:
                dom = Domain.objects.get(domain=domain)
                tenant = dom.tenant
            except Domain.DoesNotExist:
                raise CommandError(f"No Domain found matching '{domain}'")

        if schema:
            try:
                tenant = Client.objects.get(schema_name=schema)
            except Client.DoesNotExist:
                raise CommandError(f"No tenant found with schema '{schema}'")

        if not tenant:
            raise CommandError("Could not resolve tenant")

        schema_name = tenant.schema_name
        self.stdout.write(self.style.SUCCESS(f"➡️  Populating tenant schema: {schema_name}"))

        with schema_context(schema_name):
            # Import models inside schema context
            from apps.core.models import (
                GeneralDetails,
                Service,
                TeamMember,
                Testimonial,
                FAQ,
                GalleryImage,
            )
            from apps.booking.models import Package, Addon

            # General details
            general_values = {
                'site_name': tenant.name or 'Home Services',
                'tagline': 'Your local pros',
                'hero_title': 'Reliable Home Services On Your Schedule',
                'hero_subtitle': 'Full-service home repairs, maintenance, and upgrades handled by licensed professionals with upfront pricing and friendly support.',
                'phone': '(555) 123-4567',
                'email': 'hello@homeservices.com',
                'address': '123 Main St, Your City',
                'footer_text': 'Trusted home improvement partner since 2010.',
            }
            general, created = GeneralDetails.objects.update_or_create(
                site_name=general_values['site_name'],
                defaults={**general_values, 'current': True},
            )
            if created:
                self.stdout.write(self.style.SUCCESS('  • GeneralDetails created'))
            else:
                self.stdout.write(self.style.SUCCESS('  • GeneralDetails updated'))

            # Services (list of tuples: (slug, name, description))
            services = [
                ('plumbing', 'Plumbing', 'Repairs, fixture upgrades, repiping, water heaters, and emergency calls.'),
                ('electrical', 'Electrical', 'Panel upgrades, lighting, EV chargers, troubleshooting, and smart installs.'),
                ('remodeling', 'Remodeling', 'Kitchens, baths, flooring, and whole-home refreshes with design support.'),
                ('maintenance', 'Maintenance Plans', 'Seasonal tune-ups, safety checks, and VIP scheduling for members.'),
            ]
            for idx, (slug, name, desc) in enumerate(services):
                svc, _ = Service.objects.update_or_create(
                    slug=slug,
                    defaults={'name': name, 'description': desc, 'order': idx, 'current': True},
                )
            self.stdout.write(self.style.SUCCESS(f'  • {len(services)} services ensured'))

            # Team members
            members = [
                ('Alex Rivera', 'Founder · GC License #12345'),
                ('Priya Patel', 'Lead Designer · NKBA Certified'),
                ('Jordan Lee', 'Service Manager · Master Plumber'),
                ('Sasha Kim', 'Electrical Lead · NABCEP Certified'),
            ]
            for idx, (name, role) in enumerate(members):
                TeamMember.objects.update_or_create(
                    name=name,
                    defaults={'role': role, 'order': idx, 'current': True},
                )
            self.stdout.write(self.style.SUCCESS(f'  • {len(members)} team members ensured'))

            # Testimonials
            testis = [
                ('Maria L.', 'Incredible service from start to finish. They handled our kitchen remodel flawlessly and stayed on budget.', 5),
                ('Dana & Chris R.', 'Responsive, professional, and transparent pricing. Our go-to team for routine maintenance.', 5),
                ('Jamal H.', 'Called for an emergency leak and they were at our door in under an hour. Highly recommend.', 5),
            ]
            for author, text, rating in testis:
                Testimonial.objects.update_or_create(
                    author=author,
                    defaults={'text': text, 'rating': rating, 'current': True},
                )
            self.stdout.write(self.style.SUCCESS(f'  • {len(testis)} testimonials ensured'))

            # FAQs
            faqs = [
                ('Do you offer same-day appointments?', 'Yes, call before noon for availability. Emergency calls are prioritized.'),
                ('Are estimates free?', 'On-site assessments and written estimates are complimentary.'),
                ('What warranties do you provide?', 'Labor guaranteed for 12 months with manufacturer coverage on parts.'),
            ]
            for idx, (q, a) in enumerate(faqs):
                FAQ.objects.update_or_create(question=q, defaults={'answer': a, 'order': idx, 'current': True})
            self.stdout.write(self.style.SUCCESS(f'  • {len(faqs)} faqs ensured'))

            # Gallery placeholders
            gallery = [
                ('Bathroom Remodel', 'https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=800&q=80'),
                ('Kitchen Upgrade', 'https://images.unsplash.com/photo-1505693314120-0d443867891c?auto=format&fit=crop&w=800&q=80'),
            ]
            for idx, (title, url) in enumerate(gallery):
                GalleryImage.objects.update_or_create(title=title, defaults={'image_url': url, 'order': idx, 'current': True})
            self.stdout.write(self.style.SUCCESS(f'  • {len(gallery)} gallery images ensured'))

            # Packages
            pkgs = [
                ('essential', 'Essential Handyman', 'Perfect for punch lists and light repairs you need handled fast.', 'one_time', 189.00, 2, ['Minor plumbing & electrical fixes', 'Fixture swaps & touch-ups', 'Includes trip + materials run']),
                ('premium', 'Premium Remodel Day', 'Dedicated crew for larger projects like bathroom refreshes or flooring.', 'one_time', 749.00, 8, ['2+ specialists on-site', 'Project coordinator updates', 'Includes haul-away + cleanup']),
                ('membership', 'Total Care Membership', 'Seasonal maintenance, priority dispatching, and bundled savings.', 'annual', 129.00, 0, ['Quarterly tune-ups', 'VIP pricing on projects', 'Dedicated account manager']),
            ]
            for order, (slug, name, desc, billing, price, duration, features) in enumerate(pkgs):
                Package.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'name': name,
                        'description': desc,
                        'billing': billing,
                        'price': price,
                        'duration_hours': duration,
                        'features': features,
                        'order': order,
                        'current': True,
                    },
                )
            self.stdout.write(self.style.SUCCESS(f'  • {len(pkgs)} packages ensured'))

            # Addons
            addons = [
                ('Premium materials pickup', 40.0, 'Pickup premium materials for the job'),
                ('Same-day rush', 65.0, 'Rush scheduling to fit you the same day'),
                ('Extra cleanup crew', 25.0, 'Extra crew for thorough cleanup'),
            ]
            for name, price, desc in addons:
                Addon.objects.update_or_create(name=name, defaults={'price': price, 'description': desc, 'current': True})
            self.stdout.write(self.style.SUCCESS(f'  • {len(addons)} addons ensured'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Done populating tenant content!'))
