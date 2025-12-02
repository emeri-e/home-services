from django.contrib import admin
from . import models


@admin.register(models.GeneralDetails)
class GeneralDetailsAdmin(admin.ModelAdmin):
	list_display = ('site_name', 'current', 'updated_at')
	list_filter = ('current',)
	search_fields = ('site_name', 'tagline')


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'order', 'current')
	prepopulated_fields = {'slug': ('name',)}
	list_filter = ('current',)


@admin.register(models.TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
	list_display = ('name', 'role', 'order', 'current')
	list_filter = ('current',)


@admin.register(models.Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = ('author', 'rating', 'current')
	list_filter = ('current', 'rating')


@admin.register(models.FAQ)
class FAQAdmin(admin.ModelAdmin):
	list_display = ('question', 'order', 'current')
	list_filter = ('current',)


@admin.register(models.GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
	list_display = ('title', 'order', 'current')
	list_filter = ('current',)

