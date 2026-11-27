from django.db import models
from django.contrib.auth.models import User


class Destination(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(
    upload_to='destination_images/',
    blank=True,
    null=True
)

    def __str__(self):
        return self.name
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username



class Booking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    travel_date = models.DateField()
    persons = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default="Confirmed")
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.destination.name}"
