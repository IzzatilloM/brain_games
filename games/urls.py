"""games ilovasi URL'lari."""

from django.urls import path

from . import views

app_name = "games"

urlpatterns = [
    path("", views.game_hub, name="list"),
    path("fanlar/", views.subjects_hub, name="subjects"),
    path("fanlar/<slug:slug>/", views.subject_group, name="subject_group"),
    path("guruh/<slug:slug>/", views.group_view, name="group"),
    path("play/<slug:slug>/", views.play, name="play"),
    path("<slug:slug>/natija/", views.submit_session, name="submit"),
]
