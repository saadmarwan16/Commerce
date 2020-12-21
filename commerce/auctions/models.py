from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username} has an id of {self.id}"


class AuctionListings(models.Model):
    name = models.TextField()
    description = models.TextField()
    category = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=64, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    time_auctioned = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(upload_to="listing-image", blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioned_items")

    def __str__(self):
        return f"{self.user_id} posted {self.name} for {self.price} at {self.time_auctioned}"


class Bids(models.Model):
    price = models.DecimalField(max_digits=64, decimal_places=2)
    time_bid = models.DateTimeField(auto_now=False, auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    auction_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="item_bids")

    def __str__(self):
        return f"{self.user_id} wants {self.auction_id} for {self.price} at {self.time_bid}"


class Comments(models.Model):
    content = models.TextField()
    time_commented = models.DateTimeField(auto_now=False, auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    auction_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="item_comments")

    def __str__(self):
        return f"{self.user_id} commented {self.content} on {self.auction_id} at {self.time_commented}"


class WatchList(models.Model):
    time_watchlisted = models.DateTimeField(auto_now=False, auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlisted_items")
    auction_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="item_watchlists")

    def __str__(self):
        return f"{self.user_id} watchlisted {self.auction_id} at {self.time_watchlisted}"
