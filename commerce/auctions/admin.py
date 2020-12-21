from django.contrib import admin

# Register your models here.
from .models import User, AuctionListings, Bids, Comments, WatchList

admin.site.register(User)
admin.site.register(AuctionListings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(WatchList)