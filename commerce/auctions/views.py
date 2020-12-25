from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Bid, Comment, WatchList


# Home page, this page displays the current active listings and their information
def index(request):
    return render(request, "auctions/main-layout.html", {
        "listings": AuctionListing.objects.all()
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


# Shows a registration form and registers a user after the user is validated
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


# Either shows the creating listing page to create a new listing or create a new listing after a submit attempt
# to create a new listing
def create_listing(request, user_id):
    if request.method == "POST":
        name = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        price = request.POST["bid"]
        image = request.FILES["image"]

        # Get the user who just created the listing
        user = User.objects.get(pk=user_id)
        
        listing = AuctionListing(name=name, description=description, category=category, price=price, image=image, user=user)
        listing.save()

        return HttpResponseRedirect(reverse("listing_created"))

    return render(request, "auctions/create-listing.html")


def categories(request):
    return render(request, "auctions/categories.html")


def watchlist(request):
    return render(request, "auctions/watchlist.html")


def listing(request, id):
    user = User.objects.get(auctioned_items__id=id)
    comments = Comment.objects.filter(auction_id__id=id)
    current_bid = Bid.objects.filter(auction_id__id=id).order_by("-price")

    if len(current_bid) > 0:
        current_bid = current_bid[0]
    
    return render(request, "auctions/listing.html", {
        "listing": AuctionListing.objects.get(pk=id),
        "user_created": user.username,
        "comments": comments,
        "current_bid": current_bid
    })


# Creates listing and store it in the database
def listing_created(request):
    return render(request, "auctions/listing-created.html")


# Show all the listings that a user has created
def user_listings(request, id):
    return render(request, "auctions/user-listings.html", {
        "listings": AuctionListing.objects.filter(user_id=id)
    })


# Takes a user's comment and then add it to the database
def comment(request, listing_id, user_id):
    user_comment = request.POST["comment"]
    user = User.objects.get(pk=user_id)
    listing = AuctionListing.objects.get(pk=listing_id)

    new_comment = Comment(content=user_comment, user=user, auction=listing)
    new_comment.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing_id}))


def bid(request, listing_id, user_id):
    user_bid = request.POST["bid"]
    user_bid = float(user_bid)
    listing = AuctionListing.objects.get(pk=listing_id)

    if user_bid < listing.price:
        raise Http404("You cannot bid less than the price of the item")

    current_bid = Bid.objects.filter(auction_id__id=listing_id).order_by("-price")

    if len(current_bid) > 0:
        current_bid = current_bid[0]

        if user_bid < current_bid.price:
            raise Http404("You cannot bid less than the current bid")

    user = User.objects.get(pk=user_id)
    new_bid = Bid(price=user_bid, user=user, auction=listing)
    new_bid.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing_id}))
