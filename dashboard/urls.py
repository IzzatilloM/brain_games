"""dashboard ilovasi URL'lari."""

from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("farzand-qoshish/", views.add_child, name="add_child"),
    path("farzand/<int:child_id>/", views.child_detail, name="child_detail"),
]
