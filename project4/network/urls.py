
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("get_posts/page<int:num_page>", views.get_posts, name="get_posts"),
    path("get_posts/following/page<int:num_page>", views.get_following_posts, name="get_following_posts"),
    path("get_posts/<int:id>/page<int:num_page>", views.get_profile_posts, name="get_profile_posts"),
    path("post/<int:id>/change_like", views.change_like, name="change_like"),
    path("profile/<int:id>", views.get_profile, name="get_profile"),
    path("profile/<int:id>/change_follow", views.change_follow, name="change_follow")
]
