from django.contrib import admin
from .models import ServerUsers, Traffic, Settings

# Register your models here.
admin.site.register(ServerUsers)
admin.site.register(Traffic)
admin.site.register(Settings)
