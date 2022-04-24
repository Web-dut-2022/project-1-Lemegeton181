from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view_entry, name="view_entry"),
    path("search", views.search_entry, name="search_entry"),
    path("create_new_entry", views.new_entry, name="new_entry"),
    path("edit_entry/<str:title>", views.edit_entry, name="edit_entry"),
    path("random", views.random_entry, name="random_entry")
]
