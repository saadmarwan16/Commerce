from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListings(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=None, decimal_places=2)
    user_id = models.ForeignKey(User, ondelete=models.CASCADE, related_name="auctioned_items")
    time_auctioned = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.user_id} posted {self.name} for {self.price} at {self.time_auctioned}"


class Bids(models.Model):
    price = models.DecimalField(max_digits=None, decimal_places=2)
    time_bid = models.DateTimeField(auto_now=False, auto_now_add=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    auction_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="item_bids")

    def __str__(self):
        return f"{self.user_id} wants {self.auction_id} for {self.price} at {self.time_bid}"


class Comments(models.Model):
    content = models.CharField(max_length=1280)
    time_commented = models.DateTimeField(auto_now=False, auto_now_add=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    auction_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="item_comments")

    def __str__(self):
        return f"{self.user_id} commented {self.content} on {self.auction_id} at {self.time_commented}"


class WatchList(models.Model):
    user_id = models.ForeignKey(User)
    time_watchlisted = models.DateTimeField(auto_now=False, auto_now_add=False)
    auction_id = models.ForeignKey(AuctionListings, ondelete=models.CASCADE, related_name="item_watchlists")

    def __str__(self):
        return f"{self.user_id} watchlisted {self.auction_id} at {self.time_watchlisted}"
