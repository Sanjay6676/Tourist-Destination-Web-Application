from django.contrib import admin
from .models import Destinations, DestinationImages, Profile, FavDestination
# Register your models here.

admin.site.register(Profile)
admin.site.register(Destinations)
admin.site.register(DestinationImages)
admin.site.register(FavDestination)