from django.db import models


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Package(TimeStampedModel):
	BILLING_CHOICES = [
		('one_time', 'One-time'),
		('monthly', 'Monthly'),
		('annual', 'Annual'),
	]

	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	billing = models.CharField(max_length=20, choices=BILLING_CHOICES, default='one_time')
	duration_hours = models.PositiveSmallIntegerField(default=1)
	features = models.JSONField(blank=True, null=True)
	order = models.PositiveIntegerField(default=0)
	current = models.BooleanField(default=True)

	class Meta:
		ordering = ['order', 'name']

	def __str__(self):
		return self.name


class Addon(TimeStampedModel):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
	description = models.TextField(blank=True)
	current = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.name} (+${self.price})"


class Booking(TimeStampedModel):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('confirmed', 'Confirmed'),
		('cancelled', 'Cancelled'),
		('completed', 'Completed'),
	]

	customer_name = models.CharField(max_length=255)
	phone = models.CharField(max_length=64, blank=True)
	email = models.EmailField(blank=True)
	service_address = models.CharField(max_length=512, blank=True)

	package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
	addons = models.ManyToManyField(Addon, blank=True)

	service_date = models.DateField(blank=True, null=True)
	arrival_window = models.CharField(max_length=64, blank=True)
	notes = models.TextField(blank=True)

	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

	def __str__(self):
		return f"Booking #{self.id} — {self.customer_name} ({self.status})"

