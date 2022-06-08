from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:TITLE>", views.entry, name="entry")
    # path("search", views.search, name="search")
]