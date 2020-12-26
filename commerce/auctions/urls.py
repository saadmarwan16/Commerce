from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist<int:listing_id>", views.watchlist, name="watchlist"),
    path("listing-created", views.listing_created, name="listing_created"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("user-listings", views.user_listings, name="user_listings"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close-auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("auction-closed", views.auction_closed, name="auction_closed"),
]
