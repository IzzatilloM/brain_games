"""core ilovasi URL'lari."""

from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("til/<str:code>/", views.set_lang, name="set_lang"),
    path("platforma/", views.about, name="about"),
    path("yordam/", views.help_page, name="help"),
    path("multipleyer/", views.multiplayer, name="multiplayer"),
    path("uy-vazifalari/", views.homework, name="homework"),
    path("statistika/", views.stats, name="stats"),
    path("reyting/", views.rating, name="rating"),
]
