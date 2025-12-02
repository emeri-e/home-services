from django.views import View
from django.shortcuts import render, get_object_or_404

from .models import Package


class BookingView(View):
	def get(self, request):
		packages = Package.objects.filter(current=True).order_by('order')
		return render(request, 'booking.html', {'packages': packages})


class CheckoutView(View):
	def get(self, request):
		slug = request.GET.get('package')
		package = None
		if slug:
			package = Package.objects.filter(slug=slug, current=True).first()

		# try to include general details if the core app is available
		general = None
		try:
			from apps.core.models import GeneralDetails
			general = GeneralDetails.objects.filter(current=True).order_by('-updated_at').first()
		except Exception:
			general = None

		return render(request, 'checkout.html', {'package': package, 'general': general})

