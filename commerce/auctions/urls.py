from django.urls import path

from . import views

urlpatterns = [
    path("", views.active_listings, name="active_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("active_listings/<int:category_id>", views.active_listings, name="active_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/update", views.update_watchlist, name="update_watchlist"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/close_listing", views.close_listing, name="close_listing"),
    path("listing/<int:listing_id>/new_bid", views.new_bid, name="new_bid"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment")
]
