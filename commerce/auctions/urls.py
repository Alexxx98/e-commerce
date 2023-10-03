from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.view_listing, name="listing"),
    path("listings/<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("listings/<int:listing_id>/close", views.close, name="close"),
    path("categories", views.view_categories, name="categories"),
    path("categories/<str:category_name>", views.category_listings, name="category_listings"),
    path("watchlist", views.view_watchlist, name="view_watchlist"),
    path("watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist")
]
