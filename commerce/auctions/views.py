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


# Attempt to log the user in if the user submits the login form, otherwise display the login page
def login_view(request):

    # The user attempts to submit the login form
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

    # The user attempts to view the login page
    else:
        return render(request, "auctions/login.html")


# Logs the user out and then return the user back to the home page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Attempt to register the user in if the user submits the registration form, otherwise display the register page
def register(request):

    # If the user submit the registration form
    if request.method == "POST":

        # Get the username and email the user submitted
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

        # Authenticate the user who just registered and redirect the user to the index page
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    # The user tries to display the register page
    else:
        return render(request, "auctions/register.html")


# Create a new listing if the user submits a new create listing form, otherwise display the create listing page
def create_listing(request):

    # User attempts to create a new listing
    if request.method == "POST":

        # Get the data the user entered into the form
        name = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        price = request.POST["bid"]
        image = request.FILES["image"]
        
        # Attempt to create a new listing from the above data
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

    # The user attempt to display the create listing page
    return render(request, "auctions/create-listing.html")


# Display the category the user tried to open, otherwise display the categories page for the user to choose from
def categories(request):

    # The user attempts to display a category
    if request.method == "POST":

        # Get the name of the category
        category = request.POST["name"]

        return render(request, "auctions/view-category.html", {
            "listings": AuctionListing.objects.filter(category=category, is_listing_closed=False),
            "category": category
        })

    # The user tries to display the categories page to choose from
    return render(request, "auctions/categories.html")


# Displays all the items a user has in his/her watchlist
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": AuctionListing.objects.filter(watchlist__id=request.user.id)
    })


# Adds an item to a user's watchlist
def watchlist_add(request, listing_id):

    # Identify the user who is attempting to add an item to his/her watchlist and also identify the item then add
    # the item to the user's watchlist
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.watchlist.add(request.user)

    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing_id}))


# Removes an item from a user's watchlist
def watchlist_remove(request, listing_id):

    # Identify the user who is attempting to remove an item to his/her watchlist and also identify the item then
    # remove the item to the user's watchlist
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.watchlist.remove(request.user)

    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing_id}))


# Displays all the information about a particular listing
def listing(request, id):

    # Identify the listing, the one who created it, it's comments and it's current bid
    item = AuctionListing.objects.get(pk=id)
    user = User.objects.get(auctioned_items__id=id)
    comments = Comment.objects.filter(auction_id__id=id)
    current_bid = item.current_bid
    
    return render(request, "auctions/listing.html", {
        "listing": item,
        "user_created": user.username,
        "comments": comments,
        "current_bid": current_bid,
        "is_watchlisted": item.is_watchlisted(request.user.id, id)
    })


# Displays listing created page indicate to the user the listing was successfully created
def listing_created(request):
    return render(request, "auctions/listing-created.html")


# Shows all the listings that a user has created
def user_listings(request):
    return render(request, "auctions/user-listings.html", {
        "listings": AuctionListing.objects.filter(listing_creator=request.user)
    })


# Closes an auction
def close_auction(request, listing_id):

    # Get the listing the user attempted to closed and then close it
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.close_listing()

    return HttpResponseRedirect(reverse("auction_closed"))


# Displays to the user that the listing has been closed
def auction_closed(request):
    return render(request, "auctions/auction-closed.html")


# Takes a user's comment and then add it to the database
def comment(request, listing_id):

    # Get the content of the comment
    user_comment = request.POST["comment"]
    listing = AuctionListing.objects.get(pk=listing_id)

    # Add the comment to listing of comments and save it
    new_comment = Comment(content=user_comment, user=request.user, auction=listing)
    new_comment.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing_id}))


# Attempt to place a new bid on a listing
def bid(request, listing_id):

    # Get the price of the bid and the listing the bid is placed on
    user_bid = request.POST["bid"]
    user_bid = float(user_bid)
    listing = AuctionListing.objects.get(pk=listing_id)

    # The user attempts place a bid less than original price of the item
    if user_bid < listing.price:
        raise Http404("You cannot bid less than the price of the item")

    # The user attempts to place a bid less than or equal to the current highest bid
    elif user_bid <= listing.current_bid:
        raise Http404("You cannot bid less than the current bid")

    # Create a new bid object, identify the item the bid was placed on, add it as the new highest bid and save
    # the bid
    new_bid = Bid(price=user_bid, user=request.user, auction=listing)
    current_bid = AuctionListing.objects.get(pk=listing_id)
    current_bid.update_bid(user_bid, request.user)
    new_bid.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"id": listing_id}))
