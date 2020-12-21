from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("listing-created/<int:user_id>", views.listing_created, name="listing_created"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("user-listings/<int:id>", views.user_listings, name="user_listings"),
]
