"""accounts ilovasi URL'lari."""

from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("kirish/", views.login_view, name="login"),
    path("royxat/", views.register_view, name="register"),
    path("chiqish/", views.logout_view, name="logout"),
    path("profil/", views.profile_view, name="profile"),
    path("ota-ona-nazorati/", views.parental_view, name="parental"),
    path("ota-ona-nazorati/saqlash/", views.parental_save, name="parental_save"),
]
