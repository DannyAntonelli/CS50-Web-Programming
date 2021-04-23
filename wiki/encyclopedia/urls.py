from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.entry, name="entry"),
    path("new_entry/", views.newEntry, name="new_entry"),
    path("edit/<str:entry>/", views.edit, name="edit"),
    path("random_entry/", views.randomEntry, name="random_entry"),
    path("search/", views.search, name="search")
]
