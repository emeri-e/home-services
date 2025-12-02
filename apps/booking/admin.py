from django.contrib import admin
from . import models


@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'price', 'billing', 'order', 'current')
	prepopulated_fields = {'slug': ('name',)}
	list_filter = ('billing', 'current')


@admin.register(models.Addon)
class AddonAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'current')
	list_filter = ('current',)


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('id', 'customer_name', 'service_date', 'status', 'total_price')
	list_filter = ('status',)
	search_fields = ('customer_name', 'email', 'phone')

