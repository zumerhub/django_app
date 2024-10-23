
import uuid
from django.db import models

from .consts import CARS_BRANDS, TRANSMISSION_OPTIONS
from users.models import Profile, Location
from .utils import user_listing_path

class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    brand = models.CharField(max_length=24, choices=CARS_BRANDS, default=None)
    model = models.CharField(max_length=64)
    vin = models.CharField(max_length=17)
    mileage = models.IntegerField(default=0)
    color = models.CharField(max_length=24)
    description = models.TextField()  # Fixed spelling
    engine = models.CharField(max_length=64)
    transmission = models.CharField(max_length=16, choices=TRANSMISSION_OPTIONS, default=None)  # Fixed field name
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=user_listing_path)

    def __str__(self):
        return f'{self.seller.user.username}\'s Listing - {self.model}'

