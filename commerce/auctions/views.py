from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListings, Bids, Comments, WatchList


# Home page, this page displays the current active listings and their information
def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListings.objects.all()
    })


# Either shows a login page or takes a post request from login page and the log the user in if the details
# are correct
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


# Logs the user out and then return the user back to the home page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Either shows the register page of register a new user throug a post request
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Either shows the creating listing page to create a new listing or create a new listing
def create_listing(request):
    return render(request, "auctions/create-listing.html")


def categories(request):
    return render(request, "auctions/categories.html")


def watchlist(request):
    return render(request, "auctions/watchlist.html")


def listing(request):
    return render(request, "auctions/listing.html")


def listing_created(request, user_id):
    name = request.POST["title"]
    description = request.POST["description"]
    category = request.POST["category"]
    price = request.POST["bid"]
    image = request.POST["image"]

    # Get the user who just created the listing
    print(user_id)
    user = User.objects.get(pk=user_id)
    
    listing = AuctionListings(name=name, description=description, category=category, price=price, image=image, user=user)
    listing.save()

    return render(request, "auctions/listing-created.html")


# Show all the listings that a user has created
def user_listing(request, id):
    return render(request, "auctions/user-listings.html", {
        "listings": AuctionListings.objects.get(user_id=id)
    })
