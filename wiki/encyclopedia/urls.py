from django.urls import path, re_path
from . import util
from . import views
import random

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.page , name="page"),
    path("wiki/<str:title>/edit", views.edit_page , name="edit"),
    path("create_page/", views.create_page, name="create"),
    path("random/", views.random, name="random"),
    path("search/", views.search, name="search"),
]
