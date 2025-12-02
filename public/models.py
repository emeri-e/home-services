from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import User


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password="admin1234")

class Domain(DomainMixin):
    pass
