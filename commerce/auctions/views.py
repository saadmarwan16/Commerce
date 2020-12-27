from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Bid, Comment


# Home page, this page displays the current active listings and their information
def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.filter(is_listing_closed=False)
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
def create_listing(request):
    if request.method == "POST":
        name = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        price = request.POST["bid"]
        image = request.FILES["image"]
        
        listing = AuctionListing(
            name=name,
            description=description,
            category=category,
            price=price,
            current_bid=price,
            image=image,
            listing_creator=request.user
            )

        listing.save()

        return HttpResponseRedirect(reverse("listing_created"))

    return render(request, "auctions/create-listing.html")


def categories(request):
    return render(request, "auctions/categories.html")


def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": AuctionListing.objects.filter(watchlist__id=request.user.id)
    })


def watchlist_add(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.watchlist.add(request.user)

    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing_id}))


def watchlist_remove(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.watchlist.remove(request.user)

    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing_id}))


def listing(request, id):
    user = User.objects.get(auctioned_items__id=id)
    comments = Comment.objects.filter(auction_id__id=id)
    current_bid = Bid.objects.filter(auction_id__id=id).order_by("-price")
    item = AuctionListing.objects.get(pk=id)

    if len(current_bid) > 0:
        current_bid = current_bid[0]
    
    return render(request, "auctions/listing.html", {
        "listing": item,
        "user_created": user.username,
        "comments": comments,
        "current_bid": current_bid,
        "is_watchlisted": item.is_watchlisted(request.user.id, id)
    })


# Creates listing and store it in the database
def listing_created(request):
    return render(request, "auctions/listing-created.html")


# Show all the listings that a user has created
def user_listings(request):
    return render(request, "auctions/user-listings.html", {
        "listings": AuctionListing.objects.filter(listing_creator=request.user)
    })


def close_auction(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.close_listing()

    return HttpResponseRedirect(reverse("auction_closed"))


def auction_closed(request):
    return render(request, "auctions/auction-closed.html")


# Takes a user's comment and then add it to the database
def comment(request, listing_id):
    user_comment = request.POST["comment"]
    listing = AuctionListing.objects.get(pk=listing_id)

    new_comment = Comment(content=user_comment, user=request.user, auction=listing)
    new_comment.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing_id}))


def bid(request, listing_id):
    user_bid = request.POST["bid"]
    user_bid = float(user_bid)
    listing = AuctionListing.objects.get(pk=listing_id)

    if user_bid < listing.price:
        raise Http404("You cannot bid less than the price of the item")
    elif user_bid < listing.current_bid:
        raise Http404("You cannot bid less than the current bid")

    new_bid = Bid(price=user_bid, user=request.user, auction=listing)
    new_bid.save()

    current_bid = AuctionListing.objects.get(pk=listing_id)
    current_bid.update_bid(user_bid, request.user)

    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing_id}))
