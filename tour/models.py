from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Destinations(models.Model):
    place_name = models.CharField(max_length=100, blank=False, null=False)
    p_image = models.ImageField(upload_to='p_image',blank=False,null=False)
    weather = models.CharField(max_length=50, blank=False,null=True)
    location = models.CharField(max_length=100, blank=False, null=False)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    map_link =models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.place_name

class DestinationImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='d_images/')
    review = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.destination.place_name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=50, blank=False, null=False)
    l_name = models.CharField(max_length=50, blank=True, null=True)
    contact_no = models.CharField(max_length=15, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.f_name +' '+self.l_name
    
class FavDestination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.destination.place_name