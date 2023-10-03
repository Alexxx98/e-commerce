from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bids, Comments, Categories, Watchlist

from .forms import CreateListing, PlaceBid, PostComment


users = User.objects.all()

def index(request):
    watchlist = None
    if request.user in users:
        watchlist = Watchlist.objects.get(user=request.user)
    return render(request, "auctions/index.html", {
        "items": Listing.objects.all(),
        "watchlist": watchlist,
    })


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
            watchlist = Watchlist(user=user)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create_listing(request):
    watchlist = None
    if request.user in users:
        watchlist = Watchlist.objects.get(user=request.user)
    if request.method == "POST":
        form = CreateListing(request.POST)
        category = Categories.objects.get(name=request.POST['categories'])
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.save()
            category.listing.add(listing)
            bid = Bids(
                user=request.user, listing=listing
                )
            bid.save()
            return HttpResponseRedirect(reverse("index"))
        
    return render(request, "auctions/create_listing.html", {
        "form": CreateListing(),
        "categories": Categories.objects.all(),
        "watchlist": watchlist,
    })

def view_listing(request, listing_id):
    watchlist = None
    if request.user in users:
        watchlist = Watchlist.objects.get(user=request.user)
    listing = Listing.objects.get(pk=int(listing_id))
    bid = Bids.objects.get(listing=listing)
    if request.method == "POST":
        form = PlaceBid(request.POST)
        if form.is_valid():
            value = int(form.cleaned_data['value'])
            if bid.counter == 0 and value < listing.bid:
                messages.warning(request, "Bid has to be at least price value.")
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            elif bid.counter > 0 and value <= listing.bid:
                messages.warning(request, "Bid has to be higher than price value.")
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            bid.user = request.user
            bid.value = value
            bid.counter += 1
            bid.save()
            listing.bid = bid.value
            listing.save()
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": bid,
        "form": PlaceBid(),
        "comment": PostComment(),
        "comments": listing.comments.all(),
        "category": Categories.objects.get(listing=listing),
        "watchlist": watchlist,
    })

def add_comment(request, listing_id):
    listing = Listing.objects.get(pk=int(listing_id))
    if request.method == "POST":
        form = PostComment(request.POST)
        if form.is_valid():
            author = request.user
            content = form.cleaned_data['content']
            comment = Comments(author=author, listing=listing, comment=content)
            comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def view_categories(request):
    watchlist = None
    if request.user in users:
        watchlist = Watchlist.objects.get(user=request.user)
    return render(request, "auctions/categories.html", {
        "categories": Categories.objects.all(),
        "watchlist": watchlist,
    })

def category_listings(request, category_name):
    watchlist = None
    if request.user in users:
        watchlist = Watchlist.objects.get(user=request.user)
    category = Categories.objects.get(name=category_name)
    return render(request, "auctions/category_listing.html", {
        'listings': category.listing.all(),
        "watchlist": watchlist,
    })

def close(request, listing_id):
    listing = Listing.objects.get(pk=int(listing_id))
    if request.method == "POST":
        listing.active = False
        listing.save()
    return HttpResponseRedirect(reverse("index"))

def view_watchlist(request):
    watchlist = None
    if request.user in users:
        watchlist = Watchlist.objects.get(user=request.user)
    current_user = request.user
    watchlist = Watchlist.objects.get(user=current_user)
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist.listing.all(),
        "watchlist": watchlist,
    })

def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        watchlist = Watchlist.objects.get(user=request.user)
        watchlist.listing.add(listing)
        watchlist.counter += 1
        watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
