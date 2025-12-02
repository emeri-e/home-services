from django.db import models


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class GeneralDetails(TimeStampedModel):
	"""Site-wide settings and content (hero, contact, branding, etc.).

	Multiple rows are allowed but one can be marked `current=True` to be active.
	"""
	site_name = models.CharField(max_length=255, default='Home Services Co.')
	tagline = models.CharField(max_length=255, blank=True)

	hero_title = models.CharField(max_length=255, blank=True)
	hero_subtitle = models.TextField(blank=True)
	hero_image_url = models.URLField(blank=True)
	hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)

	logo_url = models.URLField(blank=True)
	logo = models.ImageField(upload_to='logos/', blank=True, null=True)

	phone = models.CharField(max_length=64, blank=True)
	email = models.EmailField(blank=True)
	address = models.CharField(max_length=512, blank=True)

	footer_text = models.TextField(blank=True)

	map_embed_url = models.URLField(blank=True)

	current = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'General Details'

	def __str__(self):
		return f"{self.site_name} ({'current' if self.current else 'archived'})"


class Service(TimeStampedModel):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	image_url = models.URLField(blank=True)
	image = models.ImageField(upload_to='services/', blank=True, null=True)
	order = models.PositiveIntegerField(default=0)
	current = models.BooleanField(default=True)

	class Meta:
		ordering = ['order', 'name']

	def __str__(self):
		return self.name


class TeamMember(TimeStampedModel):
	name = models.CharField(max_length=200)
	role = models.CharField(max_length=200, blank=True)
	bio = models.TextField(blank=True)
	photo_url = models.URLField(blank=True)
	photo = models.ImageField(upload_to='team/', blank=True, null=True)
	order = models.PositiveIntegerField(default=0)
	current = models.BooleanField(default=True)

	class Meta:
		ordering = ['order', 'name']

	def __str__(self):
		return self.name


class Testimonial(TimeStampedModel):
	author = models.CharField(max_length=200)
	text = models.TextField()
	rating = models.PositiveSmallIntegerField(default=5)
	current = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.author} — {self.rating}★"


class FAQ(TimeStampedModel):
	question = models.CharField(max_length=512)
	answer = models.TextField()
	order = models.PositiveIntegerField(default=0)
	current = models.BooleanField(default=True)

	class Meta:
		ordering = ['order']

	def __str__(self):
		return self.question


class GalleryImage(TimeStampedModel):
	title = models.CharField(max_length=255, blank=True)
	image_url = models.URLField(blank=True)
	image = models.ImageField(upload_to='gallery/', blank=True, null=True)
	caption = models.CharField(max_length=512, blank=True)
	order = models.PositiveIntegerField(default=0)
	current = models.BooleanField(default=True)

	class Meta:
		ordering = ['order']

	def __str__(self):
		return self.title or (self.caption[:40] if self.caption else 'Gallery image')

