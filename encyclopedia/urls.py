from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("results/", views.results, name="results"),
    path("new/", views.new, name="new"),
    path("<str:title>/edit/", views.edit, name="edit"),
    path("<str:title>", views.get_entry, name="entry"),
]
