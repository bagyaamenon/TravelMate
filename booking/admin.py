from django.contrib import admin
from .models import Destination, UserProfile, Booking

admin.site.register(Destination)
admin.site.register(UserProfile)
admin.site.register(Booking)