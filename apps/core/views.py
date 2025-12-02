from django.views import View
from django.shortcuts import render

from .models import GeneralDetails, Service, TeamMember, Testimonial, FAQ, GalleryImage
try:
    # import package model if booking app is available
    from apps.booking.models import Package
except Exception:
    Package = None


class HomePageView(View):
    def get(self, request):
        # fetch the current GeneralDetails (take the most recently updated current row)
        general = GeneralDetails.objects.filter(current=True).order_by('-updated_at').first()

        services = Service.objects.filter(current=True).order_by('order')
        team = TeamMember.objects.filter(current=True).order_by('order')
        testimonials = Testimonial.objects.filter(current=True).order_by('-created_at')[:6]
        faqs = FAQ.objects.filter(current=True).order_by('order')
        gallery = GalleryImage.objects.filter(current=True).order_by('order')
        packages = Package.objects.filter(current=True).order_by('order') if Package is not None else None

        context = {
            'client_name': getattr(general, 'site_name', getattr(request.tenant, 'name', 'Home Services')),
            'general': general,
            'services': services,
            'team': team,
            'testimonials': testimonials,
            'faqs': faqs,
            'gallery': gallery,
            'packages': packages,
        }
        return render(request, 'index.html', context)
