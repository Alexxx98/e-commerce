from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authors")
    description = models.TextField()
    bid = models.FloatField(default=0)
    image = models.URLField()
    time = models.DateTimeField(default=timezone.now())
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Author: {self.author}, Item: {self.title}, bid: {self.bid}"


class Bids(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, default=0, on_delete=models.CASCADE, related_name="bids")
    value = models.FloatField(default=0)
    counter = models.IntegerField(default=0)


class Comments(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(default="", max_length=300)


class Categories(models.Model):
    name = models.CharField(max_length=64)
    listing = models.ManyToManyField(Listing, blank=True, related_name="listings")

    def __str__(self):
        return f"{self.name} {self.listing}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    listing = models.ManyToManyField(Listing, blank=True, related_name="watch_listings")
    counter = models.IntegerField(default=0)
