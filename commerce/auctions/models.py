from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return self.category


class Listing(models.Model):
    # Listing's informations
    title = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    expired = models.BooleanField(default=False)
    photo_url = models.CharField(max_length=100000, blank=True, null=True)

    # Price
    starting_price = models.FloatField()
    current_offer = models.FloatField(blank=True, null=True)

    # Users
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_opened")
    buyer = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    watchers = models.ManyToManyField(User, blank=True, related_name="watching")

    def __str__(self):
        return str(self.id) + ": " + self.title


class Bid(models.Model):
    offer = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")