from django.urls import path
from . import views

urlpatterns = [
    path("player/", views.player),
    path("player/<int:pk>/", views.player),
    path("match/", views.match),
    path("match/<int:pk>/", views.match),
    path("stream/", views.stream, name="stream"),
]
