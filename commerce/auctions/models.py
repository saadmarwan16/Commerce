from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username} has an id of {self.id}"


class AuctionListing(models.Model):
    name = models.TextField()
    description = models.TextField()
    category = models.CharField(max_length=64)
    is_listing_closed = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=64, decimal_places=2)
    current_bid = models.DecimalField(max_digits=64, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    time_auctioned = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(upload_to="listing-image/", blank=True, null=True)
    watchlist = models.ManyToManyField(User, related_name="watchlisted_items")
    listing_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioned_items")
    listing_winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True, blank=True)
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="highest_bid", null=True, blank=True)

    def __str__(self):
        return f"{self.listing_creator} posted {self.name} for {self.price} at {self.time_auctioned}"

    def update_bid(self, bid, bidder):
        self.current_bid = bid
        self.highest_bidder = bidder
        self.save()

    def close_listing(self):
        self.listing_winner = self.highest_bidder
        self.is_listing_closed = True
        self.save()

    def is_watchlisted(user):
        try:
            result = AuctionListing.objects.get(watchlist="user")
            return result
        except AuctionListing.DoesNotExist:
            return False


class Bid(models.Model):
    price = models.DecimalField(max_digits=64, decimal_places=2)
    time_bid = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="item_bids")

    def __str__(self):
        return f"{self.user_id} wants {self.auction_id} for {self.price} at {self.time_bid}"


class Comment(models.Model):
    content = models.TextField()
    time_commented = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="item_comments")

    def __str__(self):
        return f"{self.user_id} commented {self.content} on {self.auction_id} at {self.time_commented}"


# class WatchList(models.Model):
#     time_watchlisted = models.DateTimeField(auto_now=False, auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlisted_items")
#     auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="item_watchlists")

#     def __str__(self):
#         return f"{self.user_id} watchlisted {self.auction_id} at {self.time_watchlisted}"
