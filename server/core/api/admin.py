from django.contrib import admin
from .models import Client, Traffic, Settings

# Register your models here.
admin.site.register(Client)
admin.site.register(Traffic)
admin.site.register(Settings)
